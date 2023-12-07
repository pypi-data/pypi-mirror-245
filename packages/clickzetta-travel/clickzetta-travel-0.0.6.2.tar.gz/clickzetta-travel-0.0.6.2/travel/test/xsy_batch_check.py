import os.path
import random
import sys
import json
from datetime import datetime
from time import sleep
import sqlite3
import travel.util.validation_util as validation_util
from migration.connector.source.mysql.source import MysqlSource
from migration.connector.source.pg.source import PGSource
from concurrent.futures import ThreadPoolExecutor, CancelledError, wait, ALL_COMPLETED
from migration.connector.destination.clickzetta.destination import ClickZettaDestination
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

global_result_map = {}

real_time_table_ddl = ('create table xsy_validation (id integer primary key autoincrement, source_table varchar(255), '
                       'dest_table varchar(255), source_count integer, '
                       'dest_count integer, only_in_source integer, '
                       'only_in_dest integer, only_in_source_list text, only_in_dest_list text,'
                       ' only_source_max_times_id text, only_dest_max_times_id text,'
                       'check_timestamp text, max_source_db_time text, last_check_status varchar(255))')

select_pattern = 'select only_in_source_list,only_in_dest_list from xsy_validation where source_table = ? and dest_table = ?'

update_pattern = ('update xsy_validation set source_count = ?, dest_count = ?, last_check_status = ?, only_in_source = ?, only_in_dest = ?, '
                  'only_in_source_list = ?, only_in_dest_list = ?,only_source_max_times_id = ?, only_dest_max_times_id = ?'
                  ' ,check_timestamp = ?, max_source_db_time = ?'
                  'where source_table = ? and dest_table = ?')

insert_pattern = ('insert into xsy_validation (source_table, dest_table, source_count, dest_count,last_check_status, only_in_source, '
                  'only_in_dest, only_in_source_list, only_in_dest_list,only_source_max_times_id, only_dest_max_times_id,'
                  ' check_timestamp, max_source_db_time)'
                  ' values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')

delete_pattern = 'delete from xsy_validation where source_table = ? and dest_table = ?'

def _format_job_id():
    unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                       + str(random.randint(10000, 99999))
    return format_unique_id


def write_validation_table_result(source_df_result, destination_df_result, out_path, source_table, destination_table, uid:str):
    print(f'processing {source_table} and {destination_table}')
    try:
        if source_df_result.equals(destination_df_result):
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is equal with {destination_table} result.\n')
        else:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is not equal with {destination_table} result. \n')
            diff_result = source_df_result.sort_index().sort_index(axis=1).compare(destination_df_result.sort_index().sort_index(axis=1),
                                                                                   result_names=(source_table,
                                                                                                 destination_table))
            with open(f'{out_path}/{uid}_diff_result.csv', 'a') as f:
                f.write(diff_result.to_csv(index=True))
    except Exception as e:
        raise e

def check_validation(source, destination, source_table, destination_table, out_path, uid,
                     validation_type, check_schema=0, pk_cols=None,
                     cdc_event_table_prefix=None, sqlite_db_file_path=None):
    source_df_result = None
    destination_df_result = None
    if check_schema:
        check_schema_result = validation_util.schema_table_validation(source, destination, source_table, destination_table)
        only_in_source_cols = check_schema_result['only_in_source_cols']
        only_in_destination_cols = check_schema_result['only_in_dest_cols']
        if len(only_in_source_cols) > 0 or len(only_in_destination_cols) > 0:
            with open(f'{out_path}/{uid}_diff_schema_result.txt', 'a') as f:
                f.write(
                    f'{source_table} has columns {only_in_source_cols} not in {destination_table}.\n')
                f.write(
                    f'{destination_table} has columns {only_in_destination_cols} not in {source_table}.\n')
    if int(validation_type) == 0:
        source_df_result, destination_df_result = validation_util.gen_basic_validation_table_result(source, destination, source_table, destination_table)
    elif int(validation_type) == 1:
        source_df_result, destination_df_result = validation_util.multidimensional_validation_table(source, destination, source_table, destination_table)
    elif int(validation_type) == 2:
        diff_result = validation_util.data_diff_table_validation(source, destination, source_table, destination_table)
        if len(diff_result) == 0:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is equal with {destination_table} result.\n')
        else:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is not equal with {destination_table} result. \n')

            with open(f'{out_path}/{uid}_diff_result.csv', 'a') as f:
                for line in diff_result:
                    f.write(line)
            return
    elif int(validation_type) == 3:
        source_df_result, destination_df_result = validation_util.count_table_validation(source, destination, source_table, destination_table)
    elif int(validation_type) == 4:
        logger.info(f'processing {source_table} and {destination_table}')
        try:
            source_count, dest_count, abs_count = validation_util.count_table_validation_without_df(source, destination, source_table, destination_table)
            if abs_count == 0:
                with sqlite3.connect(sqlite_db_file_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(delete_pattern, (source_table, destination_table))
                logger.info(f'{source_table} and {destination_table} are equal.Source_count: {source_count}, dest_count: {dest_count}')
                return
            assert pk_cols is not None, 'pk_cols is None'
            if abs_count > 0:
                check_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                assert cdc_event_table_prefix is not None, 'cdc_event_table_prefix is None'
                cdc_evnt_table_name = f'{cdc_event_table_prefix}_{destination_table.split(".")[0]}_{destination_table.split(".")[1]}_clickzetta_cdc_event'
                schema_name = destination_table.split('.')[0]
                max_cdc_time = int(destination.execute_sql(f'select max(op_ts) from {schema_name}.`{cdc_evnt_table_name}`')[0][0])
                max_cdc_time_str = datetime.fromtimestamp(max_cdc_time/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
                result_dict = validation_util.pk_id_table_validation_with_count(source, destination, source_table, destination_table, pk_cols, abs_count)
                result_dict['source_count'] = source_count
                result_dict['dest_count'] = dest_count
                result_dict['check_timestamp'] = check_timestamp
                map_key = f'{source_table}-{destination_table}'
                if map_key not in global_result_map:
                    global_result_map[map_key] = []
                global_result_map[map_key].append(result_dict)
                status = 'DONE' if result_dict['check_status'] == 1 else 'UN_DONE'
                with sqlite3.connect(sqlite_db_file_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(select_pattern, (map_key.split('-')[0], map_key.split('-')[1]))
                    result = cursor.fetchall()
                    if len(result) == 0:
                        if int(result_dict['only_in_source']) == 0 and int(result_dict['only_in_dest']) == 0:
                            return
                        source_entries = ','.join('%s' %(str(entry).strip()) for entry in result_dict['only_in_source_list'])
                        if len(result_dict['only_in_source_list']) > 0:
                            source_entries = '1-{' + source_entries + '}'
                        dest_entries = ','.join('%s' %(str(entry).strip()) for entry in result_dict['only_in_dest_list'])
                        if len(result_dict['only_in_dest_list']) > 0:
                            dest_entries = '1-{' + dest_entries + '}'
                        cursor.execute(insert_pattern, (map_key.split('-')[0], map_key.split('-')[1], result_dict['source_count'],
                                                        result_dict['dest_count'], status, result_dict['only_in_source'],
                                                        result_dict['only_in_dest'], source_entries, dest_entries,
                                                        '1',
                                                        '1',
                                                        result_dict['check_timestamp'], max_cdc_time_str))
                        return
                    assert len(result) == 1, 'sqlite3 result length is not 1'
                    for row in result:
                        only_in_source_list,only_in_dest_list = row
                    source_map = {}
                    dest_map = {}
                    for entry in only_in_source_list.strip().split('|'):
                        count = int(entry.split('-')[0])
                        entries = entry.split('-')[1][1:][:-1].split(',')
                        for item in entries:
                            source_map[str(item).strip()] = count
                    for entry in only_in_dest_list.strip().split('|'):
                        if len(entry) == 0:
                            continue
                        count = int(entry.split('-')[0])
                        entries = entry.split('-')[1][1:][:-1].split(',')
                        for item in entries:
                            dest_map[str(item).strip()] = count

                    former_source_set = set(source_map.keys())
                    former_dest_set = set(dest_map.keys())
                    now_source_set = set(str(entry).strip() for entry in result_dict['only_in_source_list'])
                    now_dest_set = set(str(entry).strip() for entry in result_dict['only_in_dest_list'])
                    diff_source = former_source_set - now_source_set
                    diff_dest = former_dest_set - now_dest_set

                    for entry in result_dict['only_in_source_list']:
                        if str(entry) in source_map:
                            source_map[str(entry)] += 1
                        else:
                            source_map[str(entry)] = 1
                    for entry in result_dict['only_in_dest_list']:
                        if str(entry) in dest_map:
                            dest_map[str(entry)] += 1
                        else:
                            dest_map[str(entry)] = 1
                    for entry in diff_source:
                        source_map.pop(entry)
                    for entry in diff_dest:
                        dest_map.pop(entry)
                    sorted_source = sorted(source_map.items(), key=lambda x: x[1], reverse=True)
                    sorted_dest = sorted(dest_map.items(), key=lambda x: x[1], reverse=True)
                    temp_source_map = {}
                    temp_dest_map = {}
                    for index, entry in enumerate(sorted_source):
                        if entry[1] not in temp_source_map:
                            temp_source_map[entry[1]] = [str(entry[0]).strip()]
                        else:
                            temp_source_map[entry[1]].append(str(entry[0]).strip())
                    for index, entry in enumerate(sorted_dest):
                        if entry[1] not in temp_dest_map:
                            temp_dest_map[entry[1]] = [str(entry[0]).strip()]
                        else:
                            temp_dest_map[entry[1]].append(str(entry[0]).strip())
                    new_source_item = []
                    new_dest_item = []
                    for key,value in temp_source_map.items():
                        new_source_item.append(str(key) + '-{' + ','.join('%s' %(entry) for entry in value) + '}')

                    for key,value in temp_dest_map.items():
                        new_dest_item.append(str(key) + '-{' + ','.join('%s' %(entry) for entry in value) + '}')
                    cursor.execute(update_pattern, (result_dict['source_count'], result_dict['dest_count'],
                                                    status, result_dict['only_in_source'],
                                                    result_dict['only_in_dest'], '|'.join('%s' %(entry) for entry in new_source_item),
                                                    '|'.join('%s' %(entry) for entry in new_dest_item),
                                                    new_source_item[0].split('-')[0] if len(new_source_item) > 0 else ''
                                                    , new_dest_item[0].split('-')[0] if len(new_dest_item) > 0 else '',
                                                    result_dict['check_timestamp'],
                                                    max_cdc_time_str, map_key.split('-')[0], map_key.split('-')[1]))
            return
        except Exception as e:
            logger.error('real-time validation error:', e)
    elif int(validation_type) == 5:
        try:
            result_dict = validation_util.pk_id_table_validation(source, destination, source_table, destination_table, pk_cols)
            with open(f'{out_path}/{uid}_{source_table}_full_table_check_result.txt', 'a') as f:
                f.write(f"{source_table} AND {destination_table} full table check result:\n")
                f.write(f"only_in_source_pk_count: {result_dict['only_in_source']}\n")
                f.write(f"only_in_dest_pk_count: {result_dict['only_in_dest']}\n")
                f.write(f"only_in_source_pks: {result_dict['only_in_source_list']}\n")
                f.write(f"only_in_dest_pks: {result_dict['only_in_dest_list']}\n")
                f.write("\n")
        except Exception as e:
            logger.error('full table validation error:', e)
        return
    else:
        raise Exception(f"Unsupported validation type {validation_type}")
    write_validation_table_result(source_df_result, destination_df_result, out_path, source_table, destination_table, uid)

def validate(source, destination, source_tables, destination_tables,
             validation_type, out_path, executor, check_schema=0, pk_cols=None):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    try:
        for source_table, destination_table in zip(source_tables, destination_tables):
            executor.submit(check_validation, source, destination, source_table, destination_table,
                            out_path, uid, validation_type, check_schema, pk_cols)
    except Exception as e:
        raise e
def real_time_validate(source, destination, source_tables, destination_tables,
                       validation_type, out_path, executor, check_schema=0,
                       check_times=1, wait_time_sce=1, pk_cols=None,
                       cdc_event_table_prefix=None, sqlite_db_file_path=None):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    try:
        for i in range(check_times):
            future_results = []
            for source_table, destination_table in zip(source_tables, destination_tables):
                future = executor.submit(check_validation, source, destination, source_table,
                                         destination_table, out_path, uid, validation_type,
                                         check_schema, pk_cols, cdc_event_table_prefix, sqlite_db_file_path)
                future_results.append(future)
            wait(future_results, None, return_when=ALL_COMPLETED)
            sleep(wait_time_sce)
        with open(f'{out_path}/{uid}_real_time_result.txt', 'a') as f:
            for key, value in global_result_map.items():
                f.write(f"{key}:\n")
                for index, result_dict in enumerate(value):
                    f.write(f"check {index + 1} times, check timestamp: {result_dict['check_timestamp']}:\n")
                    f.write(f"source count: {result_dict['source_count']}\n")
                    f.write(f"dest count: {result_dict['dest_count']}\n")
                    f.write(f"only_in_source_pk_count: {result_dict['only_in_source']}\n")
                    f.write(f"only_in_dest_pk_count: {result_dict['only_in_dest']}\n")
                    f.write(f"only_in_source_pks: {result_dict['only_in_source_list']}\n")
                    f.write(f"only_in_dest_pks: {result_dict['only_in_dest_list']}\n")
                f.write("\n")
        logger.info(f"real-time validation result has been finished, please check {out_path}/{uid}_real_time_result.txt")
    except Exception as e:
        print('real-time validation error:', e)
        raise e
def get_source_connection_params(source_engine_conf):
    host = source_engine_conf['host']
    port = source_engine_conf['port']
    username = source_engine_conf['username']
    password = source_engine_conf['password']
    db_type= source_engine_conf['db_type']
    database = source_engine_conf['database']
    return {
        'host': host,
        'port': port,
        'user': username,
        'password': password,
        'db_type': db_type,
        'database': database,
    }

def get_destination_connection_params(destination_engine_conf):
    service = destination_engine_conf['service']
    workspace = destination_engine_conf['workspace']
    instance = destination_engine_conf['instance']
    vcluster = destination_engine_conf['vcluster']
    username = destination_engine_conf['username']
    password = destination_engine_conf['password']
    schema = destination_engine_conf['schema']
    instance_id = destination_engine_conf['instanceId']

    return {
        'service': service,
        'workspace': workspace,
        'instance': instance,
        'vcluster': vcluster,
        'username': username,
        'password': password,
        'schema': schema,
        'instanceId': instance_id,
    }

def construct_source_engine(connection_dict: dict):
    db_type = connection_dict['db_type']
    if db_type == 'mysql':
        return MysqlSource(connection_dict)
    elif db_type == 'postgres':
        return PGSource(connection_dict)
    else:
        raise Exception(f"Unsupported db type {db_type}")

def construct_destination_engine(connection_dict: dict):
    return ClickZettaDestination(connection_dict)


def get_source_tables(source_tables_file):
    source_tables = []
    with open(source_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            source_tables.append(line.strip())
    return source_tables

def get_destination_tables(destination_tables_file):
    destination_tables = []
    with open(destination_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            destination_tables.append(line.strip())
    return destination_tables


if __name__ == '__main__':
    source_engine_conf = sys.argv[1]
    destination_engine_conf = sys.argv[2]
    source_tables_file = sys.argv[3]
    destination_tables_file = sys.argv[4]
    validation_type = sys.argv[5]
    out_path = sys.argv[6]
    concurrency = int(sys.argv[7])
    check_schema = 0
    pk_cols = None
    check_times = 1
    wait_time_sce = 1
    cdc_event_table_prefix = None
    sqlite_db_file_path = None
    if len(sys.argv) == 9:
        check_schema = int(sys.argv[8])
    if int(validation_type) == 4:
        check_schema = int(sys.argv[8])
        pk_cols = sys.argv[9].strip()
        check_times = int(sys.argv[10])
        wait_time_sce = int(sys.argv[11])
        cdc_event_table_prefix = sys.argv[12].strip()
        sqlite_db_file_path = sys.argv[13].strip()
    if int(validation_type) == 5:
        check_schema = int(sys.argv[8])
        pk_cols = sys.argv[9].strip()
    try:
        sqlite_db_exists = os.path.exists(sqlite_db_file_path)
        with sqlite3.connect(sqlite_db_file_path) as conn:
            if not sqlite_db_exists:
                conn.execute(real_time_table_ddl)
        executor = ThreadPoolExecutor(max_workers=concurrency)
        source_engine_conf = json.load(open(source_engine_conf))
        source = construct_source_engine(get_source_connection_params(source_engine_conf))
        destination_engine_conf = json.load(open(destination_engine_conf))
        destination = construct_destination_engine(get_destination_connection_params(destination_engine_conf))
        if int(validation_type) == 5:
            source_tables = source_tables_file.split(',')
            destination_tables = destination_tables_file.split(',')
        else:
            source_tables = get_source_tables(source_tables_file)
            destination_tables = get_destination_tables(destination_tables_file)
        if int(validation_type) == 4:
            assert sqlite_db_file_path is not None, 'sqlite_db_file_path is None'
            real_time_validate(source, destination, source_tables, destination_tables, validation_type,
                               out_path, executor, check_schema, check_times,
                               wait_time_sce, pk_cols, cdc_event_table_prefix, sqlite_db_file_path)
        else:
            validate(source, destination, source_tables, destination_tables, validation_type, out_path, executor, check_schema, pk_cols)
        executor.shutdown(wait=True)
    except Exception as e:
        print('validation error:', e)
        raise e
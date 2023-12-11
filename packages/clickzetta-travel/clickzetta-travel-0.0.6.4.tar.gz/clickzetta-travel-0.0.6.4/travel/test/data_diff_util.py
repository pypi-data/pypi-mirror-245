import math
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
from migration.util import validation_table_util
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

def check_validation(source, destination, source_table, destination_table, uid, pks_str):
    try:
        result = validation_table_util.data_diff_validation_with_pks(source_table, destination_table,
                                                                     source, destination, pks_str)
        for value in result:
            print(value + '\n')
    except Exception as e:
        print(f'data-diff check validation error: {e}')
        raise e

def validate(source, destination, source_tables, destination_tables, executor, pks_str):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    try:
        for source_table, destination_table in zip(source_tables, destination_tables):
            executor.submit(check_validation, source, destination, source_table, destination_table, uid, pks_str)
    except Exception as e:
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
    concurrency = int(sys.argv[5])
    pks_str = sys.argv[6]

    try:
        executor = ThreadPoolExecutor(max_workers=concurrency)
        source_engine_conf = json.load(open(source_engine_conf))
        source = construct_source_engine(get_source_connection_params(source_engine_conf))
        destination_engine_conf = json.load(open(destination_engine_conf))
        destination = construct_destination_engine(get_destination_connection_params(destination_engine_conf))
        source_tables = get_source_tables(source_tables_file)
        destination_tables = get_destination_tables(destination_tables_file)
        validate(source, destination, source_tables, destination_tables, executor, pks_str)
        executor.shutdown(wait=True)
    except Exception as e:
        print('validation error:', e)
        raise e
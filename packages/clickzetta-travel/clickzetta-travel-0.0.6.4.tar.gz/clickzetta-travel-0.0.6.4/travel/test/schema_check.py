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
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

real_time_table_ddl = ('create table xsy_schema_validation (id integer primary key autoincrement, source_table varchar(255), '
                       'dest_table varchar(255), cols_only_in_source text, '
                       'cols_only_in_dest text,'
                       'check_timestamp text, cdc_table_count integer)')
select_pattern = 'select cols_only_in_source,cols_only_in_dest from xsy_schema_validation where source_table = ? and dest_table = ?'

update_pattern = ('update xsy_schema_validation set cols_only_in_source = ?, cols_only_in_dest = ?, check_timestamp = ?, cdc_table_count = ? '
                  'where source_table = ? and dest_table = ?')

insert_pattern = ('insert into xsy_schema_validation (source_table, dest_table, cols_only_in_source, cols_only_in_dest,'
                  ' check_timestamp, cdc_table_count)'
                  ' values (?, ?, ?, ?, ?, ?)')

delete_pattern = 'delete from xsy_schema_validation where source_table = ? and dest_table = ?'

def _format_job_id():
    unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                       + str(random.randint(10000, 99999))
    return format_unique_id

def check_validation(source, destination, source_table, destination_table, uid, sqlite_db_path, cdc_table_prefix):
    try:
        logger.info(f'processing {source_table} and {destination_table}')
        check_schema_result = validation_util.schema_table_validation(source, destination, source_table, destination_table)
        only_in_source_cols = check_schema_result['only_in_source_cols']
        only_in_destination_cols = check_schema_result['only_in_dest_cols']
        if len(only_in_source_cols) > 0 or len(only_in_destination_cols) > 0:
            cdc_evnt_table_name = f'{cdc_table_prefix}_{destination_table.split(".")[0]}_{destination_table.split(".")[1]}_clickzetta_cdc_event'
            schema_name = destination_table.split('.')[0]
            cdc_table_count = destination.execute_sql(f'select count(1) from {schema_name}.`{cdc_evnt_table_name}`')[0][0]
            with sqlite3.connect(sqlite_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(select_pattern, (source_table, destination_table))
                result = cursor.fetchone()
                if result:
                    cursor.execute(update_pattern, (','.join(only_in_source_cols),
                                                    ','.join(only_in_destination_cols),
                                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                    cdc_table_count,
                                                    source_table, destination_table))
                else:
                    cursor.execute(insert_pattern, (source_table, destination_table,
                                                    ','.join(only_in_source_cols),
                                                    ','.join(only_in_destination_cols),
                                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                    cdc_table_count))
        else:
            with sqlite3.connect(sqlite_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(delete_pattern, (source_table, destination_table))
    except Exception as e:
        print(f'schema check validation error: {e}')
        raise e
    except BaseException as e:
        print(f'schema check validation error: {e}')
        raise e

def validate(source, destination, source_tables, destination_tables, executor, sqlite_db_path, cdc_table_prefix):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    try:
        for source_table, destination_table in zip(source_tables, destination_tables):
            executor.submit(check_validation, source, destination,
                            source_table, destination_table, uid, sqlite_db_path, cdc_table_prefix)
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
    sqlite_db_path = sys.argv[6]
    cdc_table_prefix = sys.argv[7]

    try:
        sqlite_db_exists = os.path.exists(sqlite_db_path)
        with sqlite3.connect(sqlite_db_path) as conn:
            if not sqlite_db_exists:
                conn.execute(real_time_table_ddl)
        executor = ThreadPoolExecutor(max_workers=concurrency)
        source_engine_conf = json.load(open(source_engine_conf))
        source = construct_source_engine(get_source_connection_params(source_engine_conf))
        destination_engine_conf = json.load(open(destination_engine_conf))
        destination = construct_destination_engine(get_destination_connection_params(destination_engine_conf))
        source_tables = get_source_tables(source_tables_file)
        destination_tables = get_destination_tables(destination_tables_file)
        validate(source, destination, source_tables, destination_tables, executor, sqlite_db_path, cdc_table_prefix)
        executor.shutdown(wait=True)
    except Exception as e:
        print('validation error:', e)
        raise e
import streamlit as st
import sqlite3
import pandas as pd


st.set_page_config(
    page_title="Realtime Data Validation for XSY",
    layout="wide",
)


sqlite_db_file_path_pg = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_pg.db'
sqlite_db_file_path_mysql_2 = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_mysql.db'
sqlite_db_file_path_mysql_1 = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_mysql_1.db'

select_pattern = 'select * from xsy_validation '

st.markdown(
    """
    ### Clickzetta real-time data validation tool.


    - source_table: source table name
    - dest_table: destination table name
    - source_count: source table row count
    - dest_count: destination table row count
    - only_in_source: row_count only in source table
    - only_in_dest: row_count only in destination table
    - only_in_source_list: PKs only in source table, x-{pks} means pks are not in destination table occured x times
    - only_in_dest_list: PKs only in destination table, x-{pks} means pks are not in source table occured x times
    - only_source_max_times_id: max PKs missing times of only_in_source_list
    - only_dest_max_times_id: max PKs missing times of only_in_dest_list
    - check_timestamp: check timestamp
    - max_source_db_time: dest table max cdc time

"""
)

st.subheader('PgSQL Validation Result')
result_list_pg = []

with sqlite3.connect(sqlite_db_file_path_pg) as conn:
    cursor = conn.cursor()
    cursor.execute(select_pattern)
    result = cursor.fetchall()
    for row in result:
        result_list_pg.append(row)

df_pg = pd.DataFrame(result_list_pg, columns=['id', 'source_table', 'dest_table', 'source_count',
                                              'dest_count', 'only_in_source', 'only_in_dest',
                                              'only_in_source_list','only_in_dest_list','only_source_max_times_id', 'only_dest_max_times_id', 'check_timestamp', 'max_cdc_ts'])
st.dataframe(df_pg, width=3000, height=3000)


st.subheader('MySQL_2 Validation Result')
result_list_mysql = []

with sqlite3.connect(sqlite_db_file_path_mysql_2) as conn:
    cursor = conn.cursor()
    cursor.execute(select_pattern)
    result = cursor.fetchall()
    for row in result:
        result_list_mysql.append(row)

df_mysql = pd.DataFrame(result_list_mysql, columns=['id', 'source_table', 'dest_table', 'source_count',
                                                    'dest_count', 'only_in_source', 'only_in_dest',
                                                    'only_in_source_list','only_in_dest_list','only_source_max_times_id', 'only_dest_max_times_id', 'check_timestamp', 'max_cdc_ts'])
st.dataframe(df_mysql, width=3000, height=1000)


st.subheader('MySQL_1 Validation Result')
result_list_mysql_1 = []

with sqlite3.connect(sqlite_db_file_path_mysql_1) as conn:
    cursor = conn.cursor()
    cursor.execute(select_pattern)
    result = cursor.fetchall()
    for row in result:
        result_list_mysql_1.append(row)
df_mysql_1 = pd.DataFrame(result_list_mysql_1, columns=['id', 'source_table', 'dest_table', 'source_count',
                                                        'dest_count', 'only_in_source', 'only_in_dest',
                                                        'only_in_source_list','only_in_dest_list','only_source_max_times_id', 'only_dest_max_times_id', 'check_timestamp', 'max_cdc_ts'])
st.dataframe(df_mysql_1, width=3000, height=1000)
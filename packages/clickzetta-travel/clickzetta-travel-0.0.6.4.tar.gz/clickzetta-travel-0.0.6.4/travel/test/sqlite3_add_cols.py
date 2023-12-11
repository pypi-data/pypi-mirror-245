import sqlite3


sqlite_db_file_path_pg = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_pg.db'
sqlite_db_file_path_mysql_2 = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_mysql.db'
sqlite_db_file_path_mysql_1 = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_mysql_1.db'

add_cols_pattern = "alter table xsy_validation add column last_check_status varchar(255) default ''"

with sqlite3.connect(sqlite_db_file_path_pg) as conn:
    cursor = conn.cursor()
    cursor.execute(add_cols_pattern)


with sqlite3.connect(sqlite_db_file_path_mysql_2) as conn:
    cursor = conn.cursor()
    cursor.execute(add_cols_pattern)


with sqlite3.connect(sqlite_db_file_path_mysql_1) as conn:
    cursor = conn.cursor()
    cursor.execute(add_cols_pattern)

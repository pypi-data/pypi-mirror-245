import logging
import sqlite3
import time
import requests

sqlite_db_file_path_pg = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_pg.db'
sqlite_db_file_path_mysql_2 = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_mysql.db'
sqlite_db_file_path_mysql_1 = '/home/xsy/real_time_sqlite_db/real_time_validation_v2_mysql_1.db'
feishu_hook = 'https://open.feishu.cn/open-apis/bot/v2/hook/57099f8b-61e9-4243-a226-02c6975805b7'
headers = {
    "Content-Type": "application/json",
}
logger = logging.getLogger(__name__)

def check():
    while True:
        try:
            pg_results = []
            mysql_1_results = []
            mysql_2_results = []
            with sqlite3.connect(sqlite_db_file_path_pg) as conn:
                cursor = conn.cursor()
                cursor.execute('select * from xsy_validation order by only_source_max_times_id desc limit 5')
                result = cursor.fetchall()
                for row in result:
                    pg_results.append([row[1], row[2], row[9], row[10]])

            with sqlite3.connect(sqlite_db_file_path_mysql_1) as conn:
                cursor = conn.cursor()
                cursor.execute('select * from xsy_validation order by only_source_max_times_id desc limit 5')
                result = cursor.fetchall()
                for row in result:
                    mysql_1_results.append([row[1], row[2], row[9], row[10]])
            with sqlite3.connect(sqlite_db_file_path_mysql_2) as conn:
                cursor = conn.cursor()
                cursor.execute('select * from xsy_validation order by only_source_max_times_id desc limit 5')
                result = cursor.fetchall()
                for row in result:
                    mysql_2_results.append([row[1], row[2], row[9], row[10]])
            data = {
                "msg_type": "text",
                "content": {
                    "text": f"pg:\n{pg_results}\nmysql_1:\n{mysql_1_results}\nmysql_2:\n{mysql_2_results}"
                }
            }
            r = requests.post(feishu_hook, headers=headers, json=data)
            logger.info(r.json)
            break
            #time.sleep(1200)
        except Exception as e:
            print(e)
            time.sleep(1200)


if __name__ == '__main__':
    check()

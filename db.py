# 与数据库交互，存入提交信息的ID和提交时间
import pymysql
import requests

from config import user, project, table_name, password, database, sql_user
from bot import get_pr_len, get_pr_time

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user=sql_user,
    password=password,
    database=database,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

table_name = table_name

len = get_pr_len(user, project)

# 删除已存在的表，如果存在
with conn.cursor() as cursor:
    sql = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(sql)

# 初始化表
with conn.cursor() as cursor:
    sql = f"CREATE TABLE {table_name} (id INT PRIMARY KEY, time INT)"
    cursor.execute(sql)

# 遍历数据并插入数据库
for item in range(len):
    url = f'https://www.gitlink.org.cn/api/{user}/{project}/pulls.json'
    response = requests.get(url).json()
    id = response["issues"][item]["pull_request_id"]
    time = get_pr_time(user, project)[item]
    print(f"find id {id} with {time} seconds lasting...")
    # 执行SQL插入语句
    with conn.cursor() as cursor:
        sql = f"INSERT INTO {table_name} (id, time) VALUES (%s, %s)"
        cursor.execute(sql, (id, time))

# 关闭连接
conn.commit()
conn.close()

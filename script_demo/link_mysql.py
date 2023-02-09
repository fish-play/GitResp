"""
-*- coding: utf-8 -*-
@Time : 2023/1/11 10:19
"""
from wheels.mysql_wheel import Connection
db = Connection(
    '172.29.46.84',
    'demo',
    'root',
    '123456'
)
# 获取一条记录
sql = 'select * from test_table where id=%s'
data = db.get(sql, 5)
print(data)

# 获取多天记录
sql = 'select * from test_table where id>%s'
data = db.query(sql, 2)

# 插入一条数据
sql = 'insert into test_table(title, url) values(%s, %s)'
last_id = db.execute(sql, 'test', 'http://a.com/')
# 或者
last_id = db.insert(sql, 'test', 'http://a.com/')


# 使用更高级的方法插入一条数据
item = {
    'title': 'test',
    'url': 'http://a.com/',
}
last_id = db.table_insert('test_table', item)
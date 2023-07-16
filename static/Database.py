import pymysql

conn = pymysql.connect(host='127.0.0.1'  # 连接名称，默认127.0.0.1
                       , user='root'  # 用户名
                       , passwd='Lipeiru129688'  # 密码
                       , port=3306  # 端口，默认为3306
                       , db='RoamAssistant'  # 数据库名称
                       , charset='utf8'  # 字符编码
                       )
cur = conn.cursor()  # 生成游标对象
sql = "select * from City"  # SQL语句
city_name = "Beijing"
sql_1 = "SELECT city_id FROM City WHERE city_name = '%s' " % (city_name)
print(sql_1)
cur.execute(sql_1)  # 执行SQL语句
data = cur.fetchall()  # 通过fetchall方法获得数据
for d in data:  # 打印输出前2条数据
    print(d)
    print(d[0])
    print(type(d[0]))

sql_2 = "SELECT * FROM Attraction WHERE city_id = %d ORDER BY score DESC LIMIT 3;" % (d[0])
cur.execute(sql_2)
data = cur.fetchall()
for d in data:
    print(d)
cur.close()  # 关闭游标
conn.close()  # 关闭连接

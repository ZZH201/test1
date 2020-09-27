import pymysql
def conn_mysql():
    #1、建立连接
    conn = pymysql.connect(host='localhost', port=3306, user='root',
    password='root', db='ttttt', charset='utf8')
    #2.创建游标
    cur = conn.cursor()
    #3.执行sql语句
    #cur.execute('select * from test')
    id = 3
    sql = "select * from test where id = '%s'"%id
    #result = cur.fetchall()#查询所有符合条件数据
    r = cur.execute(sql)#返回查询成功的记录数
    cur.close()
    conn.close()
    print(r)
if __name__ == '__main__':
    conn_mysql()

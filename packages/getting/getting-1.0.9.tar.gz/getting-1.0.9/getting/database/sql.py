import pymysql


def query(cursor, sql):
    "pymysql 查询"
    # 执行查询
    execute = cursor.execute(sql)
    # 获取查询结果
    results = cursor.fetchall()
    return execute, results

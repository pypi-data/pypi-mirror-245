def query(cursor, sql, is_execute=False):
    "pymysql 查询"
    # 执行查询
    execute = cursor.execute(sql)
    if execute < 0:
        execute = None
    # 获取查询结果
    results = None
    if is_execute is not None:
        results = cursor.fetchall()
    return execute, results

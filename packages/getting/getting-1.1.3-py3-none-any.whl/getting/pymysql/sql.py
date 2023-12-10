def query(cursor, sql, params=None, is_execute=False):
    "pymysql 查询"
    # 执行查询
    if params is not None:
        execute = cursor.execute(sql, params)
    else:
        execute = cursor.execute(sql)
    # 获取查询结果
    results = None
    if is_execute is False:
        results = cursor.fetchall()
    return execute, results

import MySQLdb


def db_connect():
    host = "localhost"
    user = "root"
    password = "123"
    db = "myDB"
    return MySQLdb.connect(host, user, password, db, init_command='set names UTF8')


def db_insert_or_delete_or_update(query, query_params):
    try:
        conn = db_connect()
        conn.autocommit(False)
        with conn:
            cursor = conn.cursor()
            conn.begin()
            cursor.execute(query, query_params)
            conn.commit()
            cursor.close()
        conn.close()
    except MySQLdb.Error:
        conn.rollback()
        raise MySQLdb.Error("db: update or insert error")
    return


def db_select(query, query_params):
    try:
        conn = db_connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, query_params)
            result = cursor.fetchall()
            cursor.close()
        conn.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("db: select error")
    return result


def db_exist(entity, entity_attr, attr_value):
    entity_counter = db_select(
        'SELECT COUNT(id) FROM ' + entity + ' WHERE ' + entity_attr + ' = %s', (attr_value, )
    )
    if not entity_counter[0][0]:
        raise Exception(
            "db: record from table " + entity + " with " + entity_attr + " = " + str(attr_value) + "not found"
        )
    return


def db_clear():
    try:
        conn = db_connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE Followers")
            cursor.execute("TRUNCATE TABLE Forums")
            cursor.execute("TRUNCATE TABLE Posts")
            cursor.execute("TRUNCATE TABLE Subscriptions")
            cursor.execute("TRUNCATE TABLE Threads")
            cursor.execute("TRUNCATE TABLE Users")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            cursor.close()
        conn.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("db: truncate table error")
    return
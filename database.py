import mariadb


class Database:
    DATA_PATH = 'data/table/'

    _conn = None
    _tables = dict()

    @staticmethod
    def connect(db_user, db_pass, db_host, db_name):
        Database._conn = mariadb.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            database=db_name,
            port=3306)

    @staticmethod
    def execute(req):
        cursor = Database._conn.cursor()
        cursor.execute(req)
        try:
            return cursor.fetchall()
        except mariadb.ProgrammingError:
            return None

    @staticmethod
    def commit():
        Database._conn.commit()

    @staticmethod
    def close():
        Database._conn.close()

    @staticmethod
    def execute_insert(req):
        Database.execute(req)
        return Database.execute('SELECT LAST_INSERT_ID()')[0][0]

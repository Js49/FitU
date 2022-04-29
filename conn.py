import pymysql

class conn:
    def __init__(self):
        pass

    def conn_mul(self, str):
        self.str = str

        dbconfig = {'host': 'localhost', 'user': 'fitu', 'password': '123', 'database': 'fitu'}
        conn = pymysql.connect(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(self.str)
        cursor.connection.commit()
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

    def conn_one(self, str):
        self.str = str

        dbconfig = {'host': 'localhost', 'user': 'fitu', 'password': '123', 'database': 'fitu'}
        conn = pymysql.connect(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(self.str)
        cursor.connection.commit()
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res

    def conn_non(self, str):
        self.str = str

        dbconfig = {'host': 'localhost', 'user': 'fitu', 'password': '123', 'database': 'fitu'}
        conn = pymysql.connect(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(self.str)
        cursor.connection.commit()
        cursor.close()
        conn.close()

import pymysql

from werkzeug.security import generate_password_hash, check_password_hash
from conn import conn


class db_select:
    def __init__(self):
        pass

    def conn_db(self):
        con = pymysql.connect(user='fitu',
                               password='sjz529WW',
                               database='fitu',
                               host='fitu.mysql.database.azure.com',
                               ssl={'ca': 'E:/ssl/DigiCertGlobalRootCA.crt.pem'})
        # con = pymysql.connect(host='localhost', user='fitu', password='123', database='fitu')
        con.autocommit(True)
        pass

    def checkout_login(self, username, password, duty):
        # cur = db_select().conn_db()
        # 登录账户加入duty 如何通过duty判断身份切换页面 duty=一个已录入duty 设置为result
        self.pwd = password
        self.name = username
        self.duty = duty
        if duty == "admin":
            admin_account_sql = "select password from account where username='%s'and type='admin'" % self.name
            # cur.execute(admin_account_sql)
            # result1 = cur.fetchall()
            res = conn().conn_one(admin_account_sql)
            if res is not None:
                flag = check_password_hash(res[0], self.pwd)
                if flag:
                    return 0
                else:
                    return 2
            else:
                return 2
        elif duty == "user":
            user_account_sql = "select password from account where username='%s' and type='user'" % self.name
            # cur.execute(student_account_sql)
            # result2 = cur.fetchall()
            res = conn().conn_one(user_account_sql)
            if res is not None:
                flag = check_password_hash(res[0], self.pwd)
                if flag:
                    return 1
                else:
                    return 2
            else:
                return 2
        else:
            return 2

    def checkout_signin(self, username, password):  # register
        self.pwd = password
        self.name = username
        str = "select username from account where username='%s'" % (self.name)
        res = conn().conn_one(str)
        if self.name == res:
            return False
        else:
            self.pwd = generate_password_hash(self.pwd)
            str = """ insert into account values(null,'%s','%s','user')  """ % (self.name, self.pwd)
            conn().conn_non(str)
            return True

    def password_reset(self, username, pwd1):
        self.username = username
        self.pwd1 = pwd1
        sql = "select * from account where username = '%s' and type = 'user';" % (self.username)
        res = conn().conn_one(sql)
        if res:
            self.pwd1 = generate_password_hash(self.pwd1)
            reset_sql = "update account set password = '%s' where username = '%s' and type = 'user';" % (
                self.pwd1, self.username)
            conn().conn_non(reset_sql)
            return 0
        else:
            return 1

    def show_user(self):
        sql = "select * from account where type = 'user'"
        res = conn().conn_mul(sql)
        return res

    # return user id
    def r_user_id(self, username):
        self.name = username
        sql = " select uid from account where username = '%s'" % self.name
        res = conn().conn_one(sql)
        return res

    def show_course(self):
        sql = "select * from course_info"
        res = conn().conn_mul(sql)
        return res

    def show_course_detail(self, cid):
        self.cid = cid
        sql = "select * from course_info WHERE cid='%s'" % int(cid)
        res = conn().conn_one(sql)
        # title = res[1]
        # c_type = res[3]
        # description = res[2]
        # pic_file = "/static/pic/" + str(res[4])
        # video_file = "/static/play/" + str(res[5])
        # return title, c_type, description, pic_file, video_file
        return res, self.cid

    def show_exercise(self):
        sql = "select * from e_store"
        res = conn().conn_mul(sql)
        return res

    def show_food(self):
        sql = "select * from f_store"
        res = conn().conn_mul(sql)
        return res

    def show_exercise_info(self):
        sql = "select * from exercise_info"
        res = conn().conn_mul(sql)
        return res

    def show_user_info(self, id):
        self.id = id
        sql = "select * from user_info where uid='%d'" % int(self.id)
        res = conn.conn_one(sql)
        return res

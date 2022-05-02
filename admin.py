from werkzeug.security import generate_password_hash

from conn import conn


class admin:
    def __init__(self):
        pass

    def admin_course_upload(self, title, c_type, description, pic_f_name, video_f_name):
        self.title = title
        self.c_type = c_type
        self.description = description
        self.pic_f_name = pic_f_name
        self.video_f_name = video_f_name
        sql = "insert into course_info(cid, title, description, type, pic_file_path, video_file_path) values(null," \
              "'%s','%s','%s','%s','%s') " % (
                  self.title, self.description, self.c_type, self.pic_f_name, self.video_f_name)
        conn().conn_non(sql)

    def admin_course_delete(self, cid):
        self.cid = cid
        sql = "delete from course_info where cid='%d'" % int(self.cid)
        conn().conn_non(sql)
        sql1 = "delete from mycourse where cid='%d'" % int(self.cid)
        conn().conn_non(sql1)

    def admin_course_modify(self, cid, title, c_type, description, pic_f_name, video_f_name):
        self.cid = cid
        self.title = title
        self.c_type = c_type
        self.description = description
        self.pic_f_name = pic_f_name
        self.video_f_name = video_f_name

        sql = "update course_info set title = '%s', description ='%s', type='%s', pic_file_path='%s', " \
              "video_file_path='%s' where cid='%d'" % (
                  self.title, self.description, self.c_type, self.pic_f_name, self.video_f_name, int(self.cid))
        conn().conn_non(sql)

    def admin_user_mod(self, uid):
        self.uid = uid
        pwd = "pbkdf2:sha256:150000$u9k95ktK$555a393c2ac783bd87051a00797a4a70de464eb8ee8390cf7d3fe781e57dcb9f"
        reset_sql = "update account set password = '%s' where uid = '%d' ;" % (pwd, int(self.uid))
        conn().conn_non(reset_sql)

    def admin_user_del(self, uid):
        self.uid = uid
        del_sql = "DELETE FROM account WHERE uid = '%d';" % (int(self.uid))
        conn().conn_non(del_sql)
        sql1 = "delete from e_store WHERE uid = '%d';" % (int(self.uid))
        sql2 = "delete from f_store WHERE uid = '%d';" % (int(self.uid))
        sql3 = "delete from mycourse WHERE uid = '%d';" % (int(self.uid))
        sql4 = "delete from user_info WHERE uid = '%d';" % (int(self.uid))
        conn().conn_non(sql1)
        conn().conn_non(sql2)
        conn().conn_non(sql3)
        conn().conn_non(sql4)

    def admin_community_del(self):
        pass

    def admin_community_view(self):
        pass

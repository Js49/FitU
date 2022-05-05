from datetime import datetime
from conn import conn


class post:
    def __init__(self):
        pass

    def post_new(self, title, content, author):
        self.title = title
        self.content = content
        self.username = author
        today = datetime.today()
        sql = "insert into post values (null, '%s', '%s', '%s', '%s')" % (
            self.username, self.title, self.content, today)
        conn().conn_non(sql)

    def post_info(self, page):
        self.page = page
        sql1 = "SELECT CEIL(COUNT(*) / 5) AS pageTotal FROM post"
        total = conn().conn_one(sql1)
        limit = (int(page) - 1) * 5
        sql = "select * from post order by date_posted limit {0},5".format(limit)
        posts = conn().conn_mul(sql)
        return posts, total

    def get_page(self, total, p):
        total = int(total[0])
        show_page = 5  # 显示的页码数
        pageoffset = 2  # 偏移量
        start = 1  # 分页条开始
        end = total  # 分页条结束

        if total > show_page:
            if p > pageoffset:
                start = p - pageoffset
                if total > p + pageoffset:
                    end = p + pageoffset
                else:
                    end = total
            else:
                start = 1
                if total > show_page:
                    end = show_page
                else:
                    end = total
            if p + pageoffset > total:
                start = start - (p + pageoffset - end)
        # 用于模版中循环
        dic = range(start, end + 1)
        return dic

    def show_detail(self, pid):
        self.pid = pid
        sql = "select * from post where id='%d'" % self.pid
        detail = conn().conn_one(sql)
        return detail

    def post_info_user(self, username, page):
        self.username = username
        self.page = page
        sql1 = "select count(*) from post where username='%s'" % self.username
        count = conn().conn_one(sql1)
        sql2 = "SELECT CEIL(COUNT(*) / 5) AS pageTotal FROM post where username='%s'" % self.username
        total = conn().conn_one(sql2)
        limit = (int(page) - 1) * 5
        sql = "select * from post where username='%s' order by date_posted limit {0},5 ".format(limit) % self.username
        posts = conn().conn_mul(sql)
        return posts, count, total

    def get_user(self, post_id):
        self.post_id = post_id
        sql = "select username from post where id='%d'" % int(self.post_id)
        user = conn().conn_one(sql)
        return user

    def del_post(self, post_id):
        self.post_id = post_id
        sql = "delete from post where id='%d'" % int(self.post_id)
        conn().conn_non(sql)


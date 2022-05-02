from conn import conn


class history:
    def __init__(self):
        pass

    def get_food_data(self, view, uid):
        self.uid = uid
        self.view = view
        if self.view == 1:
            sql1 = "select sum(calorie) as sum, date from f_store where uid ='%d' and YEARWEEK(date_format(date,'%Y-%m-%d')) = YEARWEEK(now()) group by date" % int(
                self.uid)
            res = conn().conn_mul(sql1)
            return res
        elif self.view == 2:
            sql2 = "select sum(calorie) as sum, date from f_store where uid ='%d' and YEARWEEK(date_format(date,'%Y-%m-%d')) = YEARWEEK(now())-1 group by date" % int(
                self.uid)
            res = conn().conn_mul(sql2)
            return res
        elif self.view == 3:
            sql3 = "select sum(calorie) as sum, date from f_store where uid ='%d' and date_format(date,'%Y-%m')=date_format(now(),'%Y-%m') group by date" % int(
                self.uid)
            res = conn().conn_mul(sql3)
            return res
        elif self.view == 4:
            sql3 = "select sum(calorie) as sum, date from f_store where uid ='2' and date_format(date,'%Y-%m')=date_format(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m') group by date" % int(
                self.uid)
            res = conn().conn_mul(sql3)
            return res
        else:
            cal = []
            date = []
            return cal, date

    def test(self, uid):
        self.uid = uid
        sql1 = "select sum(calorie) as sum, date from f_store where uid ='%d' and YEARWEEK(date) = YEARWEEK(now()) group by date;" % int(
            self.uid)
        sql3 = "select sum(calorie) as sum, date from f_store where uid ='%d' group by date" % int(self.uid)
        res = conn().conn_mul(sql1)
        return res

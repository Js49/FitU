import pymysql

from conn import conn


class user():
    def __init__(self):
        pass

    def show_today_record(self, id, today):
        self.uid = id
        self.today = today
        sql_exercise = "select * from e_store where date='%s' and uid='%d'" % (self.today, int(self.uid))
        sql_food = "select * from f_store where date='%s' and uid='%d'" % (self.today, int(self.uid))
        res_e = conn().conn_mul(sql_exercise)
        res_f = conn().conn_mul(sql_food)
        print(res_e, res_f)
        if res_e == () and res_f == ():
            return 0
        elif res_e == () and res_f != ():
            return 1
        elif res_f == () and res_e != ():
            return 2
        else:
            return 3

    def show_exercise_today(self, id, today):
        self.uid = id
        self.today = today
        sql = "select * from e_store where date='%s' and uid='%d'" % (self.today, int(self.uid))
        res = conn().conn_mul(sql)
        return res

    def show_food_today(self, id, today):
        self.uid = id
        self.today = today
        sql = "select * from f_store where date='%s' and uid='%d'" % (self.today, int(self.uid))
        res = conn().conn_mul(sql)
        return res

    def insert_exercise_record(self, id, date, weight, minute, eid):
        self.uid = id
        self.date = date
        self.weight = weight
        self.minute = minute
        self.eid = eid
        sql1 = "select cal_min from exercise_info where eid = '%d'" % self.eid
        cal = conn().conn_one(sql1)
        total = cal * self.minute * self.weight
        sql = "insert into e_store values (null, '%d', '%d', '%d', '%f', '%s')" % (
            int(self.uid), int(self.eid), int(self.minute), float(total), self.date)
        conn().conn_non(sql)  # 没有计算总值 --需要计算后再插入

    def insert_food_record(self, id, date, name, energy, gram):
        self.uid = id
        self.date = date
        self.name = name
        self.energy = energy
        self.gram = gram
        total = self.energy * self.gram
        sql = "insert into f_store values (null, '%d', '%s', '%f', '%s')" % (
            int(self.uid), self.name, float(total), self.date)
        conn().conn_non(sql)

    def user_add_mycourse(self, id, cid):
        self.uid = id
        self.cid = cid
        sql = "insert into mycourse values (null, '%d', '%d')" % (int(self.uid), int(self.cid))
        conn().conn_non(sql)

    def user_check_mycourse(self, id, cid):
        self.uid = id
        self.cid = cid
        sql = "select * from mycourse where uid='%d' and cid='%d'" % (int(self.uid), int(self.cid))
        flag = conn().conn_one(sql)
        return flag

    def show_course_detail(self, cid):
        self.cid = cid
        sql = "select * from course_info WHERE cid='%d'" % int(self.cid)
        res = conn().conn_one(sql)
        title = res[1]
        c_type = res[3]
        description = res[2]
        v_file = "/static/play/" + str(res[5])
        return title, c_type, description, v_file

    def user_info_update(self, id, gender, age, height, cur_weight, goal_weight):
        self.uid = id
        self.gender = gender
        self.age = age
        self.height = height
        self.cur_weight = cur_weight
        self.goal_weight = goal_weight
        sql = "update user_info set gender='%s', age='%d', height='%f', cur_weight=" \
              "%f', goal_weight='%f' where uid='%d'" % (
                  self.gender, int(self.age), float(self.height), float(self.cur_weight), float(self.goal_weight),
                  int(self.uid))
        conn().conn_non(sql)

    def user_info_insert(self, id, gender, age, height, cur_weight, goal_weight):
        self.uid = id
        self.gender = gender
        self.age = age
        self.height = height
        self.cur_weight = cur_weight
        self.goal_weight = goal_weight
        sql = "insert into user_info values('%d', '%s', '%d','%f', '%f', '%f')" % (
            int(self.uid), self.gender, int(self.age), float(self.height), float(self.cur_weight),
            float(self.goal_weight))
        conn().conn_non(sql)

    def cal_bmr(self, id, daily_exe):
        self.uid = id
        self.daily_exe = daily_exe
        sql = "select * from user_info where uid='%d'" % int(self.uid)
        res = conn().conn_one(sql)
        if res[1] == 'male':
            bmr = 10 * res[4] + 6.25 * res[3] - 5 * res[2] + 5
            # BMR (male) = 10 X weight (kg) + 6.25 X height (cm) - 5 X age (years) + 5
            tdee = bmr * float(self.daily_exe)
            return bmr, tdee
        else:
            bmr = 10 * res[4] + 6.25 * res[3] - 5 * res[2] - 161
            # BMR (female) = 10 X weight (kg) + 6.25 X height (cm) - 5 X age (years) - 161
            tdee = bmr * float(self.daily_exe)
            return bmr, tdee

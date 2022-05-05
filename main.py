import datetime
import os

from flask import *
from werkzeug.utils import secure_filename

from admin import admin
from db_select import db_select
from user import user
from history import history
from post import post

app = Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

global username, uid


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    global username, uid
    user_name = request.form.get("username", type=str)
    pwd = request.form.get("password", type=str)
    duty = request.form.get("duty_account_login", type=str)
    if not (user_name and pwd and duty):
        return render_template("login.html")
    else:
        print(user_name + pwd + duty)
        checkout = db_select().checkout_login(user_name, pwd, duty)
        if checkout == 0:
            username = user_name
            uid = db_select().r_user_id(username)[0]
            return redirect("/admin_user_manage")
        if checkout == 1:
            username = user_name
            uid = db_select().r_user_id(username)[0]
            return redirect("/userMain")
        else:
            return render_template("login.html", erro="Wrong username or password")


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    user = request.form.get("username", type=str)
    pwd1 = request.form.get("password1", type=str)
    pwd2 = request.form.get("password2", type=str)
    if not (user and pwd1 and pwd2):
        return render_template("signin.html")
    else:
        if pwd1 != pwd2:
            return render_template("signin.html", erro="The two passwords do not match")
        elif len(pwd1) < 5 or len(pwd1) > 10:
            return render_template("signin.html", erro="The length of password should be in 5 to 10")
        # elif re.match("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]$"):
        #     return render_template("signin.html", erro="The password isn't up to the mustard")
        else:
            checkout = db_select().checkout_signin(user, pwd1)
            if not checkout:
                return render_template("signin.html", erro="Username already exists")
            else:
                return redirect("/login")


@app.route('/pwdReset', methods=['POST', 'GET'])
def pwd_reset():
    username = request.form.get("username", type=str)
    pwd1 = request.form.get("newpwd", type=str)
    pwd2 = request.form.get("newpwd1", type=str)
    if not (username and pwd1 and pwd2):
        return render_template("passwordReset.html")
    else:
        if pwd1 != pwd2:
            return render_template("passwordReset.html", erro="The two passwords do not match")
        elif len(pwd1) < 5 or len(pwd1) > 10:
            return render_template("passwordReset.html", erro="The length of password should be in 5 to 10")
        else:
            checkout = db_select().password_reset(username, pwd1)
            if checkout == 1:
                return render_template("passwordReset.html", erro="Cannot find this account")
            else:
                return redirect("/login")


@app.route('/admin_user_manage', methods=['POST', 'GET'])
def admin_user_manage():
    res = db_select().show_user()
    return render_template("adminUser.html", data=res)


@app.route('/mod_user/<uid>', methods=['POST', 'GET'])
def mod_user(uid):
    admin().admin_user_mod(uid)
    return "<script>alert('Reset successfully!');location.href='/admin_user_manage';</script>"


@app.route('/del_user/<uid>', methods=['POST', 'GET'])
def del_user(uid):
    admin().admin_user_del(uid)
    return "<script>alert('Delete successfully!');location.href='/admin_user_manage';</script>"


@app.route('/admin_course_manage', methods=['POST', 'GET'])
def admin_course_manage():
    res = db_select().show_course()
    return render_template("adminCourse.html", data=res)


@app.route('/course_upload', methods=['POST', 'GET'])
def course_upload():
    title = request.form.get("title", type=str)
    c_type = request.form.get("type", type=str)
    description = request.form.get("description", type=str)

    if title and c_type and description:
        if request.method == 'POST':
            pic_f = request.files['pic_file']
            video_f = request.files['video_file']
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            pic_f_name = secure_filename(pic_f.filename)
            video_f_name = secure_filename(video_f.filename)
            upload_pic_path = os.path.join(basepath, 'static\pic', pic_f_name)
            upload_video_path = os.path.join(basepath, 'static\play', video_f_name)
            pic_f.save(upload_pic_path)
            video_f.save(upload_video_path)

            admin().admin_course_upload(title, c_type, description, pic_f_name, video_f_name)
            return redirect(url_for('admin_course_manage'))
    return render_template("adminCourseUpload.html")


@app.route('/del_course/<cid>', methods=['POST', 'GET'])
def del_course(cid):
    admin().admin_course_delete(cid)
    return redirect(url_for('admin_course_manage'))


@app.route('/mod_course/<cid>', methods=['POST', 'GET'])
def mod_course(cid):
    print(cid)
    # title, c_type, description, pic_file, video_file = db_select().show_course_detail(cid)
    # return render_template("adminCourseModify.html", cid=cid, title=title, c_type=c_type, description=description,
    #                        pic_file=pic_file, video_file=video_file)
    res, cid = db_select().show_course_detail(cid)
    return render_template("adminCourseModify.html", cid=cid, data=res)


@app.route('/mod_course_update', methods=['POST', 'GET'])
def mod_course_update():
    cid = request.form.get("cid", type=str)
    title = request.form.get("title", type=str)
    c_type = request.form.get("c_type", type=str)
    description = request.form.get("description", type=str)
    # if title and c_type and description:
    #     if request.method == 'POST':
    pic_f = request.files['pic_file']
    video_f = request.files['video_file']
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    pic_f_name = secure_filename(pic_f.filename)
    video_f_name = secure_filename(video_f.filename)
    upload_pic_path = os.path.join(basepath, 'static\pic', pic_f_name)
    upload_video_path = os.path.join(basepath, 'static\play', video_f_name)
    pic_f.save(upload_pic_path)
    video_f.save(upload_video_path)
    print(c_type)
    admin().admin_course_modify(cid, title, c_type, description, pic_f_name, video_f_name)
    return "<script>alert('success update');location.href='/admin_course_manage';</script>"
    # return render_template("adminCourseModify.html")


@app.route('/userMain')
def user_main():
    global username, uid
    print(username, uid)
    today = datetime.date.today()
    record = user().show_today_record(uid, today)
    print(record)
    if record == 0:
        return render_template('userMain.html', hint_text="You haven't upload any record yet.", username=username)
    elif record == 1:
        f_data = user().show_food_today(uid, today)
        return render_template('userMain.html', f_data=f_data,
                               e_hint_text="You haven't upload any exercise record yet.",
                               username=username)
    elif record == 2:
        e_data = user().show_exercise_today(uid, today)
        return render_template('userMain.html', e_data=e_data, f_hint_text="You haven't upload any food record yet.",
                               username=username)
    else:
        f_data = user().show_food_today(uid, today)
        e_data = user().show_exercise_today(uid, today)
        return render_template('userMain.html', f_data=f_data, e_data=e_data, username=username)


@app.route('/user_add_events', methods=['POST', 'GET'])
def user_add_events():
    global uid
    event = request.args.get("event", type=str)
    print(event)
    if event == '1':
        data = db_select().show_exercise_info()
        return render_template('record.html', event=event, data=data)
    elif event == '2':
        return render_template('record.html', event=event)
    else:
        return render_template('record.html', event=event)


@app.route('/e_record_submit', methods=['POST', 'GET'])
def e_record_submit():
    global uid
    print("hello")
    date = request.form.get("e_date", type=str)
    weight = request.form.get("weight", type=str)
    minute = request.form.get("minute", type=str)
    eid = request.form.get("eid", type=str)
    print(date, weight, minute, eid)
    user().insert_exercise_record(uid, date, weight, minute, eid)
    return "<script>alert('success insert');location.href='/user_add_events';</script>"


@app.route('/f_record_submit', methods=['POST', 'GET'])
def f_record_submit():
    global uid
    date = request.form.get("f_date", type=str)
    name = request.form.get("f_name", type=str)
    energy = request.form.get("f_energy", type=str)
    gram = request.form.get("gram", type=str)
    user().insert_food_record(uid, date, name, energy, gram)
    return "<script>alert('success insert');location.href='/user_add_events';</script>"


@app.route('/del_e_post/<rid>', methods=['POST', 'GET'])
def del_e_post(rid):
    user().del_e_post(rid)
    return redirect('/userMain')


@app.route('/del_f_post/<rid>', methods=['POST', 'GET'])
def del_f_post(rid):
    user().del_f_post(rid)
    return redirect('/userMain')


@app.route('/user_course', methods=['POST', 'GET'])
def user_course():
    data = db_select().show_course()
    return render_template('course.html', data=data)


@app.route('/add_myCourse/<cid>', methods=['POST', 'GET'])
def add_myCourse(cid):
    global uid

    flag = user().user_check_mycourse(uid, cid)
    print(flag)
    if flag is None:
        user().user_add_mycourse(uid, cid)
        return "<script>alert('you have successfully add this to your list!');location.href='/user_course';</script>"
    else:
        return "<script>alert('you have already add this to your list!');location.href='/user_course';</script>"


@app.route('/my_course', methods=['POST', 'GET'])
def my_course():
    global uid
    data = user().show_my_course(uid)
    if data is None:
        return "<script>alert('you haven't add any course yet. ');location.href='/user_course';</script>"
    return render_template('myCourse.html', data=data)


@app.route('/del_myCourse/<cid>', methods=['POST', 'GET'])
def del_mycourse(cid):
    global uid
    user().user_del_mycourse(uid, cid)
    return "<script>alert('you have successfully add this to your list!');location.href='/my_course';</script>"


@app.route('/user_courseDetail/<cid>', methods=['POST', 'GET'])
def user_course_detail(cid):
    title, c_type, description, v_file = user().show_course_detail(cid)
    return render_template('courseDetail.html', cid=cid, title=title, c_type=c_type, description=description,
                           v_file=v_file)


@app.route('/user_info', methods=['POST', 'GET'])
def user_info():
    global uid, username
    res = db_select().show_user_info(uid)
    print(res)
    # return render_template('userMyinfo.html')
    return render_template('userMyinfo.html', username=username, res=res)


@app.route('/search', methods=['POST', 'GET'])
def search():
    value = request.args.get("value", type=str)
    if not value:
        data = db_select().show_course()
        return render_template('course.html', data=data)
    else:
        data = db_select().find_course(value)
        return render_template('course.html', data=data)


@app.route('/search_my', methods=['POST', 'GET'])
def search_my():
    global uid
    value = request.args.get("value", type=str)
    if not value:
        data = user().show_my_course(uid)
        return render_template('myCourse.html', data=data)
    else:
        data = db_select().find_my_course(value, uid)
        return render_template('myCourse.html', data=data)


@app.route('/user_info_submit', methods=['POST', 'GET'])
def user_info_submit():
    global uid, username
    gender = request.form.get('radioSex', type=str)
    age = request.form.get('age', type=str)
    height = request.form.get('height', type=str)
    cur_weight = request.form.get('cur_weight', type=str)
    goal_weight = request.form.get('goal_weight', type=str)
    daily_exe = request.form.get('exercise', type=str)
    res = db_select().show_user_info(uid)
    print(res)
    if res is not None:
        user().user_info_update(uid, gender, age, height, cur_weight, goal_weight)
        bmr, tdee = user().cal_bmr_update(uid, daily_exe)
    else:
        user().user_info_insert(uid, gender, age, height, cur_weight, goal_weight)
        bmr, tdee = user().cal_bmr(uid, daily_exe)

    return render_template('userMyinfo.html', username=username, res=res, bmr=bmr, tdee=tdee)


@app.route('/history_exercise', methods=['POST', 'GET'])
def history_exercise():
    global uid
    view = request.form.get('time', type=str)
    cal = []
    date = []
    res = history().get_exercise_data(view, uid)
    if res == ():
        erro = "No record"
        return render_template('history_exercise.html', erro=erro, cal=cal, date=date)
    else:
        for i in res:
            date.append(str(i[0]))
            cal.append(str((i[1])))
        return render_template('history_exercise.html', cal=cal, date=date)


@app.route('/history_exercise_select', methods=['POST', 'GET'])
def history_exercise_select():
    global uid
    view = request.form.get('time', type=str)
    print(view)
    cal = []
    date = []
    res = history().get_exercise_data(view, uid)
    print(res)
    if res == ():
        erro = "No record"
        return render_template('history_exercise.html', erro=erro, cal=cal, date=date)
    else:
        for i in res:
            date.append(str(i[0]))
            cal.append(str((i[1])))
        return render_template('history_exercise.html', cal=cal, date=date)


@app.route('/history_food', methods=['POST', 'GET'])
def history_food():
    global uid
    view = request.form.get('time', type=str)
    cal = []
    date = []
    res = history().get_food_data(view, uid)
    if res == ():
        erro = "No record"
        return render_template('history_food.html', erro=erro, cal=cal, date=date)
    else:
        for i in res:
            date.append(str(i[0]))
            cal.append(str((i[1])))
        return render_template('history_food.html', cal=cal, date=date)


@app.route('/history_food_select', methods=['POST', 'GET'])
def history_food_select():
    global uid
    view = request.form.get('time', type=str)
    print(view)
    cal = []
    date = []
    res = history().get_food_data(view, uid)
    print(res)
    if res == ():
        erro = "No record"
        return render_template('history_food.html', erro=erro, cal=cal, date=date)
    else:
        for i in res:
            date.append(str(i[0]))
            cal.append(str((i[1])))
        return render_template('history_food.html', cal=cal, date=date)


@app.route("/postMain")
def postMain():
    global username
    page_status = 0  # 显示首页状态
    page = request.args.get('page', default=1, type=int)  # get page else go to page 1
    print(page)
    posts, total = post().post_info(page)  # display posts from database, only display 5 at a time
    dic = post().get_page(total, page)
    datas = {
        'page': int(page),
        'total': int(total[0]),
        'page_status': page_status,
        'dic_list': dic
    }
    return render_template("postMain.html", datas=datas, posts=posts)


@app.route("/add_post", methods=['GET', 'POST'])
def new_post():
    global username
    title = request.form.get('title', type=str)
    content = request.form.get('content', type=str)
    if title and content:
        post().post_new(title, content, username)
        return "<script>alert('Your post has been created ');location.href='/postMain';</script>"
    return render_template('create_post.html', legend='New Post')


@app.route("/user_post/<string:username>")
def user_post(username):
    page = request.args.get('page', 1, type=int)  # get page else go to page 1
    page_status = 0  # 显示首页状态
    posts, count, total = post().post_info_user(username, page)
    print(page)
    dic = post().get_page(total, page)
    datas = {
        'page': int(page),
        'total': int(total[0]),
        'page_status': page_status,
        'dic_list': dic
    }
    return render_template('user_post.html', datas=datas, posts=posts, count=count, user=username)


@app.route("/post_detail/<int:post_id>")  # /post/1 etc
def post_detail(post_id):
    global username
    post_detail = post().show_detail(post_id)  # give me the post with this id else give me 404 error
    return render_template('post.html', ifo=post_detail, user=username)


@app.route("/post_delete/<int:post_id>", methods=['POST'])  # /post/1 etc
def delete_post(post_id):
    global username
    user = post().get_user(post_id)  # give me the post with this id else give me 404 error
    print('aa')
    print(user)
    print(username)
    if str(user[0]) != username:
        print('bb')
        return "<script>alert('Your don't have right to delete this post ');location.href='/postMain';</script>"
    else:
        print('cc')
        post().del_post(post_id)
        print('dd')
        return "<script>alert('Your have successfully delete this post ');location.href='/postMain';</script>"


@app.route("/post_update/<int:post_id>", methods=['GET', 'POST'])  # /post/1 etc
def update_post(post_id):
    global username
    title = request.form.get('title', type=str)
    content = request.form.get('content', type=str)
    detail = post().show_detail(post_id)  # give me the post with this id else give me 404 error
    if detail[1] != username:
        return "<script>alert('Your don't have right to update this post ');location.href='/postMain';</script>"
    if title and content:
        post().post_new(title, content, username)
        return "<script>alert('Your post has been update ');location.href='/postMain';</script>"
    return render_template('create_post.html', legend='Update Post', detail=detail)


if __name__ == '__main__':
    app.run(debug=True)

from time import time
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from configparser import ConfigParser
from UserLogin import UserLogin
from dbplaceholder import FDataBase
import sqlalchemy
import os.path
import random
tasks_upload_folder = './FRONT/STATIC/Tasks'
allowed_tasks_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'raw', 'tiff', 'jp2'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_tasks_extensions

works=[{"id": 1 , "type": "Практическая","name": "Практика первых номеров егэ","status": 0 ,"stats": [0,0,0,0]},
       {"id": 2 , "type": "Практическая","name": "Практика первых номеров егэ","status": 0 ,"stats": [0,0,0,0]},
       {"id": 3 , "type": "Самостоятельная","name": "Практика первых номеров егэ","status": 1 ,"stats": [1,0,1,2]},
       {"id": 4 , "type": "Контрольная","name": "Практика первых номеров егэ","status": 2 ,"stats":[1,1,1,1]}]

tasks = [{'photo': '/STATIC/Tasks/t0e0.jpg','id': 0,'answer': 1,}, 
         {'photo': '/STATIC/Tasks/t0e1.jpg','id': 1,'answer': 2,},
         {'photo': '/STATIC/Tasks/t0e2.jpg','id': 2,'answer': 3,},
         {'photo': '/STATIC/Tasks/t0e3.jpg','id': 3,'answer': 4,}]
stats = [{'last_answer': '','is_correct': 0},
         {'last_answer': '','is_correct': 0},
         {'last_answer': '','is_correct': 0},
         {'last_answer': '','is_correct': 0}]
works_not_sorted=[{'class': random.randint(7,11), 'type': random.randint(1,3),'name':random.randint(1000,10000),'id': random.randint(1,10000)} for i in range(30)]
students_not_sorted=[{'class': random.randint(7,11) ,'id': i+1, 'name': 'Имя', 'surname': 'Фамилия'} for i in range(50)]

dbase = FDataBase()

app = Flask(__name__, template_folder='../FRONT', static_folder='../FRONT/STATIC')
app.config['UPLOAD_FOLDER'] = tasks_upload_folder
app.config['SECRET_KEY'] = 'b10c9f26110997bc68bf736fe0d41a40609f9d94'
socketio = SocketIO(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = None
login_manager.anonymous_user


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

# @socketio.on('disconnect')
# def disconnect_user():
#     logout_user()
#     session.pop('yourkey', None)


@app.route("/", methods=['GET'])
def home():
    return redirect(url_for('login'))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.get_id():
        if current_user.get_id() == 'teacher':
            return redirect("http://127.0.0.1:5000/teacher")
        else:
            return redirect("http://127.0.0.1:5000/menu")

    if request.method == 'POST':
        post = list(request.form.keys())[2]

        if request.form["log"] == "teacher":
            user = {'username': request.form['log']}
        else:
            user = {'username': request.form['log']} | dbase.getUser(request.form['log'])
        print(user)
        if post == 'enter' and request.form['pas'] == '1':
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            if request.form["log"] == "teacher":
                return redirect("http://127.0.0.1:5000/teacher")
            else:
                return redirect("http://127.0.0.1:5000/menu")
        flash(message='Ошибка авторизации. Проверьте корректность введенных данных.', category='error')
    return render_template('login.html', )

@app.route("/menu", methods=['POST', 'GET'])
@login_required
def menu():
    if current_user.get_id() == 'teacher':
        return redirect("http://127.0.0.1:5000/")
    global works
    if request.method == 'POST':
        id=int(list(request.form.keys())[0])
        print(id)
        for work in works:
                if work["id"]==id:
                    work["status"] = 2
    for work in works:
        work["stats"]=[work["stats"].count(1),len(work["stats"])]
    works_new=[x for x in works if x["status"]==0]
    works_started=[x for x in works if x["status"]==1]
    works_ended=[x for x in works if x["status"]==2]
    return render_template('index.html', works_0=works_new,works_1=works_started,works_2=works_ended)

@app.route("/work", methods=['POST', 'GET'])
@login_required
def work():
    if current_user.get_id() == 'teacher':
        return redirect("http://127.0.0.1:5000/")
    global works
    global stats
    if request.method == 'POST':
        post = list(request.form.keys())
        if int(post[0]) % 100  == 99:
            id=int(post[0])//100
            for work in works:
                if work["id"]==id:
                    print(work)
                    work["status"] = 1
            
        else:
            id=int(post[1])//100

            answer = request.form[str(post[0])]
            if answer == str(tasks[int(post[0])]['answer']) and not stats[int(post[0])]['last_answer']:
                stats[int(post[0])]['is_correct'] = 1
            elif answer == str(tasks[int(post[0])]['answer']):
                stats[int(post[0])]['is_correct'] = 2
            else:
                stats[int(post[0])]['is_correct'] = 3
            stats[int(post[0])]['last_answer'] = answer
            
        
        for i in range(len(tasks)):
            tasks[i].update(stats[i])
        
    return render_template('work.html', id=id,tasks=tasks)

@app.route("/teacher", methods=['POST', 'GET'])
@login_required
def teacher():
    if current_user.get_id() != 'teacher':
        return redirect("http://127.0.0.1:5000/")
    grade=7
    post=list(request.form.keys())
    if request.method == 'POST':
        if post[0]=="create":
            return redirect("http://127.0.0.1:5000/creation", code=302)
        elif post[-1] == "send_work":
            if len(post)>1:
                selected=post[:-1:]
            else:
                selected=[]
            print(selected)
        elif post[-1]=='create_work':
            grade=int(request.form["grade"])
            workid = time()
            print(request.form, "id: ", workid)
            tasks_index = 0
            for file in request.files.values():
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{workid}_{tasks_index}.{filename.rsplit(".", 1)[1]}'))
                    tasks_index += 1
        elif post[0][-1]=="c":
            grade=int(post[0][:-1:])
        elif post[0].isdigit():
            for i in range(len(works_not_sorted)):
                if works_not_sorted[i]["id"]==int(post[0]):
                    works_not_sorted.pop(i)
                    break
    works =[x for x in works_not_sorted if x['class']==grade]
    return render_template('teacher.html', works=works)

@app.route("/creation", methods=['POST', 'GET'])
@login_required
def creation():
    if current_user.get_id() != 'teacher':
        return redirect("http://127.0.0.1:5000/")
    return render_template('creation.html', )

@app.route("/send", methods=['POST', 'GET'])
@login_required
def send():
    if current_user.get_id() != 'teacher':
        return redirect("http://127.0.0.1:5000/")
    if request.method == 'POST':
        if list(request.form.keys())[0].isdigit():
            id=list(request.form.keys())[0]

            students=[{'class': random.randint(7,11) ,'id': i+1, 'name': 'Имя', 'surname': 'Фамилия'} for i in range(10)]
    return render_template('send.html', students=students)

@app.route("/results", methods=['POST', 'GET'])
@login_required
def results():
    if current_user.get_id() != 'teacher':
        return redirect("http://127.0.0.1:5000/")
    if request.method == 'POST':
        if list(request.form.keys())[0].isdigit():
            id=list(request.form.keys())[0]

            students=[{'class': random.randint(7,11) ,'id': i+1, 'name': 'Имя', 'surname': 'Фамилия'} for i in range(10)]
    return render_template('results.html', students=students)

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # conf = ConfigParser()
    # if not os.path.isfile('db.ini'):
    #     conf['DATABASE'] = {
    #         'IP': input('Server IP > '),
    #         'PORT': input('Server port > '),
    #         'USER': input('MySQL user > '),
    #         'PASS': input("MySQL user's password > ")}
    #     with open('db.ini', 'w') as db_conf:
    #         conf.write(db_conf)
    # else:
    #     conf.read('db.ini')
    #     conf = conf['DATABASE']
    #     ip, port, user, password = (conf['ip'], conf['port'], conf['user'], conf['pass'])
    #     db = sqlalchemy.create_engine(f'mysql://{user}:{password}@{ip}:{port}/tasks')
    #     db.connect()

    # tasks = [{'photo': f'/STATIC/Tasks/{row[1]}',
    #          'id': row[0],
    #          'answer': row[2],
    #          'last_answer': '',
    #          'is_correct': None} for row in db.execute('SELECT * FROM task0').fetchall()]

    # stats = {'completed': False, 
    #          'started': False,
    #          'correct': 0, 
    #          'answers': len(tasks)}
    app.run()

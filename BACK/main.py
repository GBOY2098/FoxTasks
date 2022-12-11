from time import time
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
from configparser import ConfigParser
import sqlalchemy
import os.path
import random

tasks_upload_folder = './FRONT/STATIC/Tasks'
allowed_tasks_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'raw', 'tiff', 'jp2'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_tasks_extensions


works_not_sorted=[{'class': random.randint(7,11), 'type': random.randint(1,3),'name':random.randint(1000,10000),'id': random.randint(1,10000)} for i in range(30)]
students_not_sorted=[{'class': random.randint(7,11) ,'id': i+1, 'name': 'Имя', 'surname': 'Фамилия', 'result': str(75)+'%'} for i in range(50)]
grade=7

app = Flask(__name__, template_folder='../FRONT', static_folder='../FRONT/STATIC')
app.config['UPLOAD_FOLDER'] = tasks_upload_folder

# @app.route("/work", methods=['POST', 'GET'])
# def work():
#     if request.method == 'POST':
#         post = list(request.form.keys())[0]
#         if post == 'start_work':
#             stats['started'] = True
#         else:
#             answer = request.form[str(post)]
#             if answer == str(tasks[int(post)]['answer']) and not tasks[int(post)]['last_answer']:
#                 tasks[int(post)]['is_correct'] = 1
#                 stats['correct'] += 1
#             elif answer == str(tasks[int(post)]['answer']):
#                 tasks[int(post)]['is_correct'] = 2
#             else:
#                 tasks[int(post)]['is_correct'] = 0
#             tasks[int(post)]['last_answer'] = answer
#     return render_template('work.html', tasks=tasks)

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        post = list(request.form.keys())[2]
        if post=="enter" and request.form["log"]=="teacher" and request.form["pas"]=="1234":
            return redirect("http://127.0.0.1:5000/teacher", code=302)
    return render_template('Login.html', )

@app.route("/menu", methods=['POST', 'GET'])
# def home():
#     if request.method == 'POST':
#         if list(request.form.keys())[0] == 'end_work':
#             stats['completed'] = True
#     return render_template('index.html', stats=stats)

@app.route("/teacher", methods=['POST', 'GET'])
def techer():
    global works_not_sorted
    global grade
    global id
    if request.method == 'POST':
        post = list(request.form.keys())[0]
        if post[-1]=="2" :
            id=post[:-1:]
            return redirect("http://127.0.0.1:5000/rezults", code=302)
        elif post[-1]=="3":
            id=post[:-1:]
            return redirect("http://127.0.0.1:5000/send", code=302)
        elif post[-1]=="4":
            for i in range(len(works_not_sorted)):
                if works_not_sorted[i]["id"]==int(post[:-1:]):
                    works_not_sorted.pop(i)
                    break
        grade=int(post)
    works =[x for x in works_not_sorted if x['class']==grade]
    return render_template('teacher.html', works=works)

@app.route("/creation", methods=['POST', 'GET'])
def creation():
    global grade
    if request.method == 'POST':
        workid = time()
        grade=int(list(request.form.keys())[0])
        if list(request.form.keys())[-1]=='create_work':
            print(request.form, "id: ", workid)
            grade=int(request.form["grade"])
            tasks_index = 0
            for file in request.files.values():
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{workid}_{tasks_index}.{filename.rsplit(".", 1)[1]}'))
                    tasks_index += 1
        return redirect("http://127.0.0.1:5000/teacher", code=302)
    return render_template('creation.html', )

@app.route("/send", methods=['POST', 'GET'])
def send():
    global grade
    students=[x for x in students_not_sorted if x['class']==grade]
    if request.method == 'POST':
        if list(request.form.keys())[-1]=='send_work':
            selected=list(request.form.keys())[:-1:]
            print(selected)
        return redirect("http://127.0.0.1:5000/teacher", code=302)
    return render_template('send.html', students=students)

@app.route("/rezults", methods=['POST', 'GET'])
def rezults():
    global grade
    students=[x for x in students_not_sorted if x['class']==grade]
    if request.method == 'POST':
        if list(request.form.keys())[-1]=='home':
            return redirect("http://127.0.0.1:5000/teacher", code=302)
    return render_template('rezults.html', students=students)

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

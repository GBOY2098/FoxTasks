from flask import Flask, render_template, request, redirect
from configparser import ConfigParser
import sqlalchemy
import os.path

works_not_sorted=[
{'class': 7, 'type': 1,'name': 'задание для малолеьних клоунов','id': 1},
{'class': 8, 'type': 2,'name': 'задание для малолеьних клоунов','id': 2},
{'class': 9, 'type': 1,'name': 'практика первых номеров ОГЭ 3','id': 3},
{'class': 10, 'type': 2,'name': 'задачки чтобы почилить после ОГЭ','id': 4},
{'class': 11, 'type': 3,'name': 'практика первых номеров ЕГЭ 1','id': 5}]
grade=7
works =[x for x in works_not_sorted if x['class']==grade]

students=[{'num': i+1, 'name': 'Имя', 'surname': 'Фамилия', 'result': str(75)+'%'} for i in range(10)]

app = Flask(__name__, template_folder='../FRONT', static_folder='../FRONT/STATIC')


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
# @app.route("/", methods=['POST', 'GET'])
# def home():
#     if request.method == 'POST':
#         if list(request.form.keys())[0] == 'end_work':
#             stats['completed'] = True
#     return render_template('index.html', stats=stats)

@app.route("/teacher", methods=['POST', 'GET'])
def techer():
    
    global grade
    if request.method == 'POST':
        post = list(request.form.keys())[0]
        if post == '7grade':
            grade=7
        elif post == '8grade':
            grade=8
        elif post == '9grade':
            grade=9
        elif post == '10grade':
            grade=10
        elif post == '11grade':
            grade=11
    works =[x for x in works_not_sorted if x['class']==grade]
    return render_template('teacher.html', works=works)

@app.route("/creation", methods=['POST', 'GET'])
def creation():
    global grade
    if request.method == 'POST':
        post = list(request.form.keys())[0]
        if list(request.form.keys())[-1]=='create_work':
            print(request.form)
            grade=int(request.form["grade"])
        if post == '7grade':
            grade=7
        elif post == '8grade':
            grade=8
        elif post == '9grade':
            grade=9
        elif post == '10grade':
            grade=10
        elif post == '11grade':
            grade=11
        works =[x for x in works_not_sorted if x['class']==grade]
        return redirect("http://127.0.0.1:5000/teacher", code=302)
    return render_template('creation.html', )

@app.route("/ckeckb", methods=['POST', 'GET'])
def ckeckb():
    return render_template('ckeckb.html', students=students)

@app.route("/rezults", methods=['POST', 'GET'])
def rezults():
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

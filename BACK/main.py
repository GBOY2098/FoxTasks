from flask import Flask, render_template, request
from configparser import ConfigParser
import sqlalchemy
import os.path


works=[
{'class': 7, 'type': 1,'name': 'задание для малолеьних клоунов','id': 1},
{'class': 8, 'type': 2,'name': 'задание для малолеьних клоунов','id': 2},
{'class': 9, 'type': 1,'name': 'практика первых номеров ОГЭ 3','id': 3},
{'class': 10, 'type': 2,'name': 'задачки чтобы почилить после ОГЭ','id': 4},
{'class': 11, 'type': 3,'name': 'практика первых номеров ЕГЭ 1','id': 5}]

works_7 =[x for x in works if x['class']==7]
works_8 =[x for x in works if x['class']==8]
works_9 =[x for x in works if x['class']==9]
works_10 =[x for x in works if x['class']==10]
works_11 =[x for x in works if x['class']==11]
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

@app.route("/teacher_7", methods=['POST', 'GET'])
def techer_7():
    return render_template('teacher_7.html', works=works_7)

@app.route("/teacher_8", methods=['POST', 'GET'])
def techer_8():
    return render_template('teacher_8.html', works=works_8)

@app.route("/teacher_9", methods=['POST', 'GET'])
def techer_9():
    return render_template('teacher_9.html', works=works_9)

@app.route("/teacher_10", methods=['POST', 'GET'])
def techer_10():
    return render_template('teacher_10.html', works=works_10)

@app.route("/teacher_11", methods=['POST', 'GET'])
def techer_11():
    return render_template('teacher_11.html', works=works_11)

@app.route("/creation", methods=['POST', 'GET'])
def creation():
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

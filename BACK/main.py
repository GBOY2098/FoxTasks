from flask import Flask, render_template, request
from configparser import ConfigParser
import sqlalchemy
import os.path

works=[{'type': 1,'name': 'практика первых номеров ЕГЭ 1','id': 1},
{'type': 2,'name': 'практика первых номеров ЕГЭ 2','id': 2},
{'type': 3,'name': 'практика первых номеров ЕГЭ 3','id': 3}]

app = Flask(__name__, template_folder='../FRONT', static_folder='../FRONT/STATIC')


@app.route("/work", methods=['POST', 'GET'])
def work():
    if request.method == 'POST':
        post = list(request.form.keys())[0]
        if post == 'start_work':
            stats['started'] = True
        else:
            answer = request.form[str(post)]
            if answer == str(tasks[int(post)]['answer']) and not tasks[int(post)]['last_answer']:
                tasks[int(post)]['is_correct'] = 1
                stats['correct'] += 1
            elif answer == str(tasks[int(post)]['answer']):
                tasks[int(post)]['is_correct'] = 2
            else:
                tasks[int(post)]['is_correct'] = 0
            tasks[int(post)]['last_answer'] = answer
    return render_template('work.html', tasks=tasks)


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if list(request.form.keys())[0] == 'end_work':
            stats['completed'] = True
    return render_template('index.html', stats=stats)

@app.route("/teacher", methods=['POST', 'GET'])
def techer_home():
    return render_template('teacher.html', works=works)

if __name__ == '__main__':
    conf = ConfigParser()
    if not os.path.isfile('db.ini'):
        conf['DATABASE'] = {
            'IP': input('Server IP > '),
            'PORT': input('Server port > '),
            'USER': input('MySQL user > '),
            'PASS': input("MySQL user's password > ")}
        with open('db.ini', 'w') as db_conf:
            conf.write(db_conf)
    else:
        conf.read('db.ini')
        conf = conf['DATABASE']
        ip, port, user, password = (conf['ip'], conf['port'], conf['user'], conf['pass'])
        db = sqlalchemy.create_engine(f'mysql://{user}:{password}@{ip}:{port}/tasks')
        db.connect()

    tasks = [{'photo': f'/STATIC/Tasks/{row[1]}',
             'id': row[0],
             'answer': row[2],
             'last_answer': '',
             'is_correct': None} for row in db.execute('SELECT * FROM task0').fetchall()]

    stats = {'completed': False, 
             'started': False,
             'correct': 0, 
             'answers': len(tasks)}

    app.run()

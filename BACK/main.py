from time import time
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from UserLogin import UserLogin
from Database import WorksDB, DataDB
import os.path


tasks_upload_folder = './FRONT/STATIC/Tasks/'
allowed_tasks_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'raw', 'tiff', 'jp2'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_tasks_extensions


app = Flask(__name__, template_folder='../FRONT', static_folder='../FRONT/STATIC')
app.config['UPLOAD_FOLDER'] = tasks_upload_folder
app.config['SECRET_KEY'] = 'b10c9f26110997bc68bf736fe0d41a40609f9d94'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = None


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


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
        user = {'username': request.form['log']}
        if post == 'enter' and dataDB.checkPass(user['username'], request.form['pas']):
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
    if request.method == 'POST':
        id=int(list(request.form.keys())[0])
        dataDB.fromInToDone(current_user.get_id(), id)

    works_new=dataDB.getNewWorks(current_user.get_id())
    works_started=dataDB.getInWorks(current_user.get_id())
    works_ended=dataDB.getDoneWorks(current_user.get_id())
    return render_template('index.html', works_0=works_new,works_1=works_started,works_2=works_ended)

@app.route("/work", methods=['POST', 'GET'])
@login_required
def work():
    userid = current_user.get_id()
    if userid == 'teacher':
        return redirect("http://127.0.0.1:5000/")

    if request.method == 'POST':
        post = list(request.form.keys())
        if int(post[0]) % 100 == 99:
            id = int(post[0]) // 100
            dataDB.fromNewToIn(userid, id)
        elif int(post[0]) % 100 == 98:
            id = int(post[0]) // 100
        else:
            id=int(post[1])//100
            tasks = worksDB.getTasks(id)
            stats = dataDB.getInWorksTasks(userid, id)

            answer = request.form[str(post[0])]
            if answer == str(tasks[int(post[0])][1]) and not stats[int(post[0])][0]:
                dataDB.changeInAnsw(userid, id, post[0], answer, 1)
                stats = dataDB.getInWorksTasks(userid, id)
                dataDB.changeInProgress(userid, id, int(sum([int(x[1]) for x in stats if int(x[1]) == 1]) / len(stats) * 100))

            elif answer == str(tasks[int(post[0])][1]):
                dataDB.changeInAnsw(userid, id, post[0], answer, 2)
            else:
                dataDB.changeInAnsw(userid, id, post[0], answer, 3)

        tasks = worksDB.getTasks(id)
        stats = dataDB.getInWorksTasks(userid, id)
        for i in range(len(tasks)):
            
            tasks[i] += stats[i]
    return render_template('work.html', id=id, tasks=tasks, range=range, len=len)

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
        elif post[-1]=='create_work':
            grade=int(request.form["grade"])
            workid = time()
            tasks_index, i = 0, 0
            paths, answers = [], []
            for file in request.files.values():
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    path = f'{workid}_{tasks_index}.{filename.rsplit(".", 1)[1]}'
                    answers.append(request.form["answer" + str(i)])
                    i += 1
                    paths.append('/STATIC/Tasks/' + path)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], path))
                    tasks_index += 1
            worksDB.addWork(request.form["name"], request.form["grade"], request.form["type"], paths, answers)
        elif post[0][-1]=="c":
            grade=int(post[0][:-1:])
        elif post[0].isdigit():
            worksDB.delWork(int(post[0]))
        elif post[0] == 'home':
            grade = 7
        elif int(post[-1]) % 100 == 99:
            id = int(post[-1]) // 100
            if len(post)>1:
                selected=post[:-1:]
            else:
                selected=[]
            dataDB.addNewWork(id, selected)
    works = worksDB.getFormWorks(grade)
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

            students = dataDB.getNumFormStudents(worksDB.getFormById(id))
    return render_template('send.html', students=students, id=id, int=int)

@app.route("/results", methods=['POST', 'GET'])
@login_required
def results():
    if current_user.get_id() != 'teacher':
        return redirect("http://127.0.0.1:5000/")
    if request.method == 'POST':
        if list(request.form.keys())[0].isdigit():
            id=list(request.form.keys())[0]

            students = dataDB.getDoneStud(id)
    return render_template('results.html', students=students)

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect("http://127.0.0.1:5000/")

@app.route("/registration", methods=['POST', 'GET'])
def registration():
    
    return render_template('registration.html', )

if __name__ == '__main__':
    worksDB, dataDB = WorksDB(), DataDB()
    # dataDB.addStudent('denis', 'Денис', 'Супер', '11Г', '12341234')
    app.run()



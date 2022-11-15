from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../FRONT', static_folder='../FRONT/STATIC')
tasks = [{'photo': '/STATIC/Tasks/Picsart_22-11-10_19-58-45-176.jpg', 'id': 0, 'answer': 'xwyz' ,'last_answer': '', 'is_correct': None},
         {'photo': '/STATIC/Tasks/Picsart_22-11-10_19-59-41-244.jpg', 'id': 1, 'answer': '36' ,'last_answer': '', 'is_correct': None},
         {'photo': '/STATIC/Tasks/Picsart_22-11-10_20-00-36-549.jpg', 'id': 2, 'answer': '46' ,'last_answer': '', 'is_correct': None},
         {'photo': '/STATIC/Tasks/Picsart_22-11-10_20-01-03-923.jpg', 'id': 3, 'answer': 'yzwx' ,'last_answer': '', 'is_correct': None},},]

stats = {'completed': False, 
         'started': False,
         'correct': 0, 
         'answers': len(tasks)}



@app.route("/work", methods=['POST', 'GET'])
def work():
    if request.method == 'POST':
        post = list(request.form.keys())[0]
        if post == 'start_work':
            stats['started'] = True
        else:
            id = post
            answer = request.form[str(id)]
            if answer == str(tasks[int(id)]['answer']) and not tasks[int(id)]['last_answer']:
                tasks[int(id)]['is_correct'] = 1
                stats['correct']+=1
            elif answer == str(tasks[int(id)]['answer']):
                tasks[int(id)]['is_correct'] = 2
            else:
                tasks[int(id)]['is_correct'] = 0
            tasks[int(id)]['last_answer'] = answer
    return render_template('work.html', tasks=tasks)

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if list(request.form.keys())[0] == 'end_work':
            stats['completed'] = True
    return render_template('index.html', stats=stats)


if __name__ == '__main__':
    app.run()

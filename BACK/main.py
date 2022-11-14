from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../FRONT', static_folder='../FRONT/STATIC')
tasks = [{'photo': '/STATIC/Tasks/Picsart_22-11-10_19-58-45-176.jpg', 'id': 0, 'answer': 0 ,'last_answer': '', 'is_correct': None},
         {'photo': '/STATIC/Tasks/Picsart_22-11-10_19-59-41-244.jpg', 'id': 1, 'answer': 1 ,'last_answer': '', 'is_correct': None},
         {'photo': '/STATIC/Tasks/Picsart_22-11-10_20-00-36-549.jpg', 'id': 2, 'answer': 2 ,'last_answer': '', 'is_correct': None},
         {'photo': '/STATIC/Tasks/Picsart_22-11-10_20-01-03-923.jpg', 'id': 3, 'answer': 3 ,'last_answer': '', 'is_correct': None},]
stats = [0, 0, len(tasks)]



@app.route("/work", methods=['POST', 'GET'])
def work():
    if request.method == 'POST':
        id = list(request.form.keys())[0]
        answer = request.form[str(id)]
        if answer == str(tasks[int(id)]['answer']) and tasks[int(id)]['last_answer']=="":
            tasks[int(id)]['is_correct'] = 0
            stats[1]+=1
        elif answer == str(tasks[int(id)]['answer']):
            tasks[int(id)]['is_correct'] = 2
        else:
            tasks[int(id)]['is_correct'] = 1
        tasks[int(id)]['last_answer'] = answer
    return render_template('work.html', tasks=tasks)

@app.route("/")
def home():
    return render_template('index.html', stats=stats)
@app.route("/complited")
def complited():
    return render_template('complited.html', stats=stats)


if __name__ == '__main__':
    app.run()

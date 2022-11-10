from flask import Flask, render_template

app = Flask(__name__, template_folder='../FRONT', static_folder='../FRONT/CSS')


@app.route("/work")
def work():
    return render_template('work.html')


@app.route("/")
def home():
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
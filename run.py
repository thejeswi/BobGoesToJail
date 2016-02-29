from flask import Flask
from flask import render_template,request, redirect,url_for
import runJudger
app = Flask(__name__)


@app.route("/template")
def template():
    return render_template('template.html')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/pseudological")
def psl():
    return render_template('pseudological.html')

@app.route("/judge", methods=['GET', 'POST'])
def judge():
    if request.method == 'GET':
        return render_template('judge_form.html')
    else:
        inputCase = request.form['inputCase']
        judgements = runJudger.run(inputCase)
        return render_template('judge_result.html', inputCase = inputCase, judgements=judgements)


if __name__ == "__main__":
    app.run(host= '0.0.0.0',port= 7070, debug=True)

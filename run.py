#!/usr/bin/env python
# coding: utf8

from flask import Flask
from flask import render_template,request, redirect,url_for
import runJudger
from pymongo import MongoClient
from pprint import pformat
from nltk import Tree
import os
from judge.judger import getLawInfo

app = Flask(__name__)
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['law_db']

@app.route("/")
def home():
    #~ return render_template('index.html')
    return redirect(url_for("judge"))

@app.route("/pseudological")
def psl():
    return render_template('pseudological.html')

@app.route("/parse_trees")
def pt():
    corenlpOut = db.parsed_laws.find()
    parseTrees = []
    for out in corenlpOut:
        sentId = str(out["sentenceID"])
        lawId = str(out["lawID"])
        for sent in out["parsed"]["sentences"]:
            pTree = sent["parsetree"]
            parseTrees.append([ pTree, sentId, lawId ])
    return render_template('parse_trees.html', parseTrees = parseTrees)

@app.route("/law_corpus")
def lc():
    laws = db.laws.find()
    lawText = []
    for law in laws:
        lawText.append(law)
    return render_template('law_corpus.html', lawText = lawText)

@app.route("/judge", methods=['GET', 'POST'])
def judge():
    if request.method == 'GET':
        return render_template('judge_form.html')
    else:
        inputCase = request.form['inputCase']
        os.system('clear')
        print "\n\n\n"
        judgements = runJudger.run(inputCase)
        relavent_laws_raw = judgements[1]
        
        relavent_laws = []
        for rlaw in relavent_laws_raw:
            law_title = getLawInfo(rlaw[1]["lawID"])
            law_title = law_title[0]+": "+law_title[1]
            relavent_laws.append((law_title, rlaw[1]["text"]))
        print relavent_laws
        
        
        judgements = judgements[0]
        return render_template('judge_result.html', inputCase = inputCase, \
            judgements=judgements, relavent_laws=relavent_laws)


if __name__ == "__main__":
    app.run(host= '0.0.0.0',port= 7070, debug=True)

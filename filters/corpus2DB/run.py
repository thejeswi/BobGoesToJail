import os
from schema import raw_law

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['raw_law']

laws_db = db.laws

def insert_law(num,title,text):
    newLaw = raw_law()
    newLaw.num = num,
    newLaw.title = title
    newLaw.text = text.split("\n")
    law_id = laws_db.insert_one(newLaw.out()).inserted_id
    return law_id

def add2db(CORPUS_FOLDER = "../../corpus/lawTexts_en/"):
    for file in os.listdir(CORPUS_FOLDER):
        if file.endswith(".txt"):
            lawText = open(CORPUS_FOLDER+file).read()
            try:
                lawTitle, lawText = lawText.split("\n", 1) #Split to only for the first line
            except ValueError:
                lawTitle = None
            lawNum = file.split(".")[0]
            print "New Entry", insert_law(lawNum, lawTitle, lawText), lawNum

if __name__=="__main__":
    add2db()

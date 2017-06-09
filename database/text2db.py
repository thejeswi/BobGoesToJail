from pymongo import MongoClient
from schema import law
from os import walk

client = MongoClient()
db = client['law_db']
corpus_path = "../corpus/lawTexts_en"
laws = db.laws
for (dirpath, dirnames, filenames) in walk(corpus_path):
    #List all the text files in the corpus path
    for one_file in filenames:
        if one_file[-3:] == "txt":
            new_law = law()
            new_law.num = one_file.split(".")[0]
            law_file = open(corpus_path+"/"+one_file)
            new_law.title = law_file.readline().strip()
            new_law.text = law_file.read().strip()
            laws.insert_one(new_law.out())
            print "Inserted ",one_file," to db"

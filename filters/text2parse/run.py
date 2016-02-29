# -- coding: utf-8 --

import ftfy
from pprint import pprint
import client
from nltk.tree import Tree
from pymongo import MongoClient

lawDB = "law_db"
dbClient = MongoClient()
lawsDB = dbClient[lawDB]
laws_db = lawsDB.laws
parse_db = lawsDB.parseTrees

def text2parsedTree(text="No sentence inputed for parsing."):
    print "Parsing text: ", text
    trees = []
    parser = client.StanfordNLP()
    result = parser.parse(text)

    # from nltk.tree import Tree
    # for sent in result['sentences']:
    #     sentence = sent['parsetree']
    #     trees.append(sentence)
    return result

def noSubLaw():
    "Return all laws with no subLaws"
    found_laws = laws_db.find({"title":{"$exists": True}})
    law_id = None
    simpleLaws = []
    for law in found_laws:
        filtered_law_texts = []
        if "title" in law:
            law_id = law["_id"]
            filtered_laws = laws_db.find({"lawID":law_id})
            count = 0
            for _law in filtered_laws:
                if "text" in _law:
                    filtered_law_texts.append(_law)
                    count += 1
            if count == 1:
                simpleLaws.extend(filtered_law_texts)

    return simpleLaws


def parsedTree2DB():
    found_laws = noSubLaw()
    count = 0
    print "Working on law number:"
    for law in found_laws:
        full_law_text = ""
        lawID = law["lawID"]
        sentenceID = law["_id"]
        lawText = ftfy.fix_text(law["text"])
        parsedText = text2parsedTree(lawText)
        parsedDict = { "lawID": lawID, "sentenceID": sentenceID, "parsed":parsedText }
        parse_db.insert_one(parsedDict)
        count += 1
        print count

if __name__ == "__main__":
    parsedTree2DB()

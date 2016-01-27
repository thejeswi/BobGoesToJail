from pprint import pprint
import client
from nltk.tree import Tree
from pymongo import MongoClient

def text2parsedTree(text="No sentence inputed for parsing."):
    print "Parsing text: ", text
    trees = []
    parser = client.StanfordNLP()
    result = parser.parse(text)
    
    for sent in result['sentences']:
        sentence = sent['parsetree']
        trees.append(sentence)
    return trees

def parsedTree2DB(lawDB = "law_db", parseDB = "parsed_laws"):
    client = MongoClient('localhost', 27017)
    lawsDB = client[lawDB]
    laws_db = lawsDB.laws    
    found_laws = laws_db.find()
    parseDB = client[parseDB]
    parse_db = parseDB.parseTrees
    for law in found_laws:
            try:
                if law["text"]:
                    print "Running lawNum: ",law["num"]
                    full_law_text = ""
                    lawID = law["_id"]
                    lawNum = law["num"]
                    print law
                    parsedText = text2parsedTree(law["text"])
                    parsedDict = { "lawID": lawID, "num":lawNum, "parsedTrees":parsedText }
                    parse_db.insert_one(parsedDict)
            except KeyError:
                print "Skipping: ", law
                continue
        
if __name__ == "__main__":
    parsedTree2DB()

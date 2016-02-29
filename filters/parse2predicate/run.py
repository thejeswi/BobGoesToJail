from schema import entity, entityLink
from treeToString import treeToString
from stringParser import stringParser as runRules
from ruleReplace import ruleReplace
import sys
from bson.objectid import ObjectId

import gc 

from pprint import pprint
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)

f = open("./output/semanticSent.json", "w")

db = client['law_db']

parsedSent = """(ROOT
  (SBARQ
    (WHNP (WP Whoever))
    (SQ
      (VP
        (PP (CC upon)
          (NP
            (NP (NN commission))
            (PP (IN of)
              (NP (DT the) (NN act)))))
        (VBZ is)
        (ADJP (JJ incapable)
          (PP (IN of)
            (S
              (VP
                (VP (VBG appreciating)
                  (NP
                    (NP (DT the) (NNS wrongfulness))
                    (PP (IN of)
                      (NP (DT the) (NN act)))))
                (CC or)
                (VP (VBG acting)
                  (PP (IN in)
                    (NP
                      (NP (NN accordance))
                      (PP (IN with)
                        (NP (JJ such) (NN appreciation)))))
                  (NP
                    (ADJP (JJ due)
                      (PP (TO to)
                        (NP
                          (NP (DT a) (JJ pathological) (JJ emotional) (NN disorder))
                          (, ,)
                          (NP
                            (NP (JJ profound) (NN consciousness) (NN disorder))
                            (, ,)
                            (NP (JJ mental) (NN defect))
                            (CC or)
                            (NP (DT any) (JJ other) (JJ serious) (JJ emotional) (NN abnormality)))
                          (, ,))))
                    (VBG acts))
                  (PP (IN without)
                    (NP (NN guilt))))))))))))
"""


i= 0

def insert_sent(tupleList, lawID, sentID):
    insertList = []
    for _entity in tupleList:
        newEntity = entity()
        newEntity.entityType = _entity[0]
        newEntity.text = _entity[1]
        newEntity.lawID = lawID
        newEntity.sentenceID = sentID
        #~ insertList.append(newEntity.out())
        if len(sys.argv)== 1:
            print(newEntity.out())
            continue
        elif sys.argv[1] == "shh":
            continue
        elif sys.argv[1] == "insert":
            #~ print "Entity:", newEntity.out()
            db.semantic_sent.insert_one(newEntity.out())
        elif sys.argv[1] == "file":
            global i
            global f
            i += 1
            f.write(str(newEntity.out())+"\n")
            f.close()

def getParseTrees():
    parseTreeList = []
    laws = db.parseTrees.find()
    #~ laws = [db.parsed_laws.find_one()]
    #~ laws = db.parsed_laws.find({"sentenceID":ObjectId("56a20255a18bdf3fadda8202")})
    #~ laws = db.parsed_laws.find({"lawID" : ObjectId("56a20255a18bdf3fadda7ffb")})
    for law in laws:
        lawID = law['lawID']
        sentenceID = law['sentenceID']
        try:
            sentences = law['parsed']['sentences']
        except KeyError:
            print "Error at", sentenceID
            continue
        for sent in sentences:
            parsedSent = runRules(str(sent['parsetree']))
            parseTreeList.append([str(parsedSent), lawID, sentenceID])
    return parseTreeList
    
def getTreeToString(pTree):
    stringList = treeToString(pTree)
    return stringList

def run():
    parseTrees = getParseTrees()
    for _pTree in parseTrees:
        sent = _pTree[0]
        print sent
        lawID = _pTree[1]
        sentID = _pTree[2]
        tupleList = getTreeToString(sent)
        #~ if "Collateral" in str(tupleList):
            #~ print "Error at:", str(tupleList)
            #~ continue
        #~ tupleList = ruleReplace(tupleList)
        insert_sent(tupleList, lawID, sentID)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "insert":
            db.semantic_sent.drop()
    run()
    #~ pprint(getParseTrees())

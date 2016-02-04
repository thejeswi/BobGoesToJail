from schema import entity, entityLink
from runRules import getParsedSentList as runRules
from treeToString import treeToString

import gc 

from pprint import pprint
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['law_db']

def insert_semantic_sent(entityList):
    lawID = entityList[1]
    sentID = entityList[2]
    for _entity in entityList[0]:
        newEntity = entity()
        newEntity.entityType = _entity[0]
        newEntity.text = _entity[1]
        newEntity.lawID = lawID
        newEntity.sentenceID = sentID
        #~ pprint(newEntity.out())
        #~ entity_db.insert_one(newEntity.out())
        #~ print newEntity.entityType,":\n",newEntity.text

def getparseTrees():
    return db.parse_tree_rules.find()

def getTreeToString(pTree):
    string = treeToString(pTree)
    return stringList

if __name__=="__main__":
    parseTrees = runRules()
    for _pTree in parseTrees:
        trees = _pTree[0]
        for tree in trees
            pprint(tree)
            break
        break

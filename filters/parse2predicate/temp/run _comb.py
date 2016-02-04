from schema import entity, entityLink, entity_simple
from stringParser import stringParser
from treeToString import treeToString

from pprint import pprint
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['tree2relations_simple']
entity_db = db.entities
entityLink_db = db.entityLinks

def insert_semantic_sent(entityList):
    lawID = entityList[1]
    sentID = entityList[2]
    newEntity = entity_simple()
    newEntity.lawID = lawID
    newEntity.sentenceID = sentID
    listOfStuff = []
    for _entity in entityList[0]:
        listOfStuff.append((_entity[0],_entity[1]))
    newEntity.text = listOfStuff
    pprint(newEntity.out())
    #~ entity_db.insert_one(newEntity.out())
    #~ raw_input()

def getLaws():
    parsedLaws = client['law_db'].parsed_laws
    return parsedLaws.find()
    
def getParsedSentList(laws):
    parsedSentList = []
    for law in laws:
        sents = law['parsed']['sentences']
        subList = []
        for sent in sents:
            parsedSent = stringParser(sent['parsetree'])
            subList.append([str(parsedSent), law["lawID"], law["sentenceID"]])
        parsedSentList.append(subList)
    return parsedSentList

def getTreeToString(parsedSentList):
    stringList = []
    for parsedSents in parsedSentList:
        subList = []
        for parsedSent in parsedSents:
            if parsedSent == None:
                continue
            string = treeToString(parsedSent[0])
            subList.append([string, parsedSent[1], parsedSent[2]])
        stringList.append(subList)
    return stringList

if __name__=="__main__":
    laws = getLaws()
    parsedSentList = getParsedSentList(laws)
    #~ pprint(parsedSentList[0])
    strings = getTreeToString(parsedSentList)
    #~ print "***************************"
    for string in strings:
        for subString in string:
            insert_semantic_sent(subString)

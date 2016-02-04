import glob
import os

from database import schema
from pymongo import MongoClient

from bson.objectid import ObjectId

#define colors
red = "\x1b[31m"
black = "\x1b[0m"
green = "\x1b[32m"
yellow = "\x1b[33m"

entColors = [('Binary', red), ('Unary', green), ('Func', yellow), ('FuncU', yellow)]

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['tree2relations_simple']
db_ent = db.entities
db_rel = db.relations


path = '/home/mlc/BobGoesToJail/corpus/lawTexts_en_simple'


def printColor(text, color):
	 print color, text, black

     
def printEntity(text, entityType):
    color = black
    for entColor in entColors:
        if entColor[0] == entityType:
            color = entColor[1]
            break
    printColor(text, color)



def printLegend():
	for entColor in entColors:
		printColor(entColor[0], entColor[1])

def printSent(obj_id):
    for _entities in db.entities.find({'sentenceID':ObjectId(obj_id)}):
	#for _entity in db.entities.find():
        #~ if not _entities['text']:
            #~ continue
        for _entity in _entities["text"]:
            entityType = _entity[0]
            text = ' '.join(_entity[1])
            print "Entity text", _entity[0]
            printEntity(text, entityType)
            #print entityType, ':', text, '\n'
        print "End of statement"
        #if text == '.':
        #	print _entity['lawID']
        
#outdated
def printRelations():
	for _rel in db_rel.find():
		fromID = _rel['EntityFromID']
		toID = _rel['EntityToID']

		fromEnt = db_ent.find_one({'_id': ObjectId(fromID)})
		toEnt = db_ent.find_one({'_id': ObjectId(toID)})

		if fromEnt and toEnt and fromEnt['text'] and toEnt['text']:
			print "from",
			printEntity(' '.join(fromEnt['text']), fromEnt['entityType'])
			print "to",
			printEntity(' '.join(toEnt['text']), toEnt['entityType'])
			print "end"
			

def printAndSavePseudoLogical(obj_id):
	outputText = ""
	uId = 0
	for _entity in db.entities.find({'sentenceID':ObjectId(obj_id)}):
		if not _entity['text']:
                        continue

		entityType = _entity['entityType']
                text = ' '.join(_entity['text'])
			
		if entityType == "Unary":
			outputText = outputText + green + 'U' + str(uId) + '(' + text + ')' + black + ' & '
			uId = uId + 1
		elif entityType == "Binary":
			outputText = outputText + red + 'B' + '(' + 'U' + str(uId - 1) + ',' + 'U' +  str(uId) + ')' + text + black + ' & '
		elif entityType == 'Func':
			label = ""
			if str(text) == 'not':
				label = 'NOT'
			outputText = outputText + yellow + label + '(' + str(text) + ')' + black + ' '

	print outputText[:-2]

def findFirstSentId(lawNum):
	dbl = client['law_db']
	lawOID =  dbl.laws.find_one({'num' : lawNum})['_id']
	print 'te', lawOID
	lawSentID = dbl.laws.find_one({'lawID': str(lawOID)})
	#return lawSentID	

lawNum = '1'
print findFirstSentId(lawNum)

sentId = '5695767ea18bdf03db4033a7'

#pipeline = [{"$group": {"_id": "$sentenceID"}}]   
#for sent in list(db.entities.aggregate(pipeline)):
if sentId:
#        sentId = sent['_id']

	print "\n===START==="
	printSent(sentId)
	print "\n==="
	#printLegend()
	print "\n==="
	#printAndSavePseudoLogical(sentId)
	#print "\n===END==="

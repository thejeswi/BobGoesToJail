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
yellow2 = "\x1b[4m"

htmlHead = """<html>
	<head>
		<title>Output Entities</title>
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>"""
htmlEnd = """</body>
</html>"""
sentenceDiv = '<div class="sentence">'
divEnd = '</div>'

entColors = [('Binary', red), ('Unary', green), ('Func', yellow), ('FuncU', yellow)]

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['tree2relations_temp']
db_ent = db.entities
db_rel = db.relations

outF = open('./outEntities/out.html', "w")
outF.write(htmlHead)

def printColor(text, color):
	 print color, text, black,

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
    for _entity in db.entities.find({'sentenceID':ObjectId(obj_id)}):
	#for _entity in db.entities.find():
        if not _entity['text']:
            continue
		
        entityType = _entity['entityType']
        text = ' '.join(_entity['text'])
        printEntity(text, entityType)
        #print entityType, ':', text, '\n'

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
			

def parseIfFinder(text):
	return text
			
			
def replaceFuncToHtml(text):
	text = text.replace('or', '&or;')
	text = text.replace('and', '&and;')
	text = text.replace('not', '&not;')
	return text
		
def getSentEntitiesArray(sent_obj_id):
	entities = []
	for _entity in db.entities.find({'sentenceID':ObjectId(sent_obj_id)}):
		if not _entity['text']:
			continue
		entities.append(_entity)
	return entities	
		
def printAndSavePseudoLogical(sent_obj_id):
	outputText = ""
	htmlText = ""
	uId = 0
	
	outF.write('<div class="sentence">')
	lawID = '-'
	law_obj_id = '-'
	sentNum = '-'
	sentType = '-'
	outF.write('<span id="sentIdentifier">Law: ' + lawID + '/' + sentNum + ' SentType: ' + sentType + '(LawID:' + law_obj_id + ' SentenceID:' + str(sent_obj_id) + '</span>')
	outF.write('<p>')
	for _entity in getSentEntitiesArray(sent_obj_id):

		entityType = _entity['entityType']
		text = ' '.join(_entity['text'])
			
		if entityType == "Unary":
			outputText = outputText + green + 'U' + str(uId) + '(' + text + ')' + black + ' & '
			outF.write('<span class="entity" id="' + entityType + '">' + 'U' + str(uId) + '(' + text + ')' + '</span>')
			uId = uId + 1
		elif entityType == "Binary":
			outputText = outputText + red + 'B' + '(' + 'U' + str(uId - 1) + ',' + 'U' +  str(uId) + ')' + text + black + ' & '
			outF.write('<span class="entity" id="' + entityType + '">' +  'B' + '(' + 'U' + str(uId - 1) + ',' + 'U' +  str(uId) + ')' + text + '</span>')
		elif entityType == 'Func':
			label = text
			outputText = outputText + yellow + label + '(' + str(text) + ')' + black + ' '	
			outF.write('<span class="entity" id="' + entityType + '">' + replaceFuncToHtml(text) + '</span>')
		elif entityType == 'FuncU':
			label = text
			outputText = outputText + yellow2 + label + '(' + str(text) + ')' + black + ' '
			outF.write('<span class="entity" id="' + entityType + '">' + replaceFuncToHtml(text) + '</span>')

	print outputText[:-2]
	outF.write('</p>')
	outF.write('<p>')
	
	outF.write('</p>')
	outF.write('</div>\n')

def findFirstSentId(lawNum):
	dbl = client['law_db']
	lawOID =  dbl.laws.find_one({'num' : lawNum})['_id']
	print 'te', lawOID
	lawSentID = dbl.laws.find_one({'lawID': str(lawOID)})
	#return lawSentID	
	
def findSent(sent_obj_id):
	dbl = client['law_db']
	return dbl.laws.find_one({'_id' : ObjectId(sent_obj_id)})

#lawNum = '1'
#print findFirstSentId(lawNum)

#sentId = '5695767ea18bdf03db4033a7'

#+ db.laws.find({'_id' : ObjectId("56a20255a18bdf3fadda81d4")})
pipeline = [{"$group": {"_id": "$sentenceID"}}]   
for sentGroups in list(db.entities.aggregate(pipeline)):

	sentId = sentGroups['_id']
	
	# sentTxtObj = findSent(sentId)
	# print "LOL", sentTxtObj, sentId
	# continue
	# lawId = sentTxtObj['lawID']
	# sentNum = sentTxtObj['num']
	# sentType = sentTxtObj['sentType']

	print "\n===START==="
	#printSent(sentId)
	print "\n==="
	#printLegend()
	print "\n==="
	printAndSavePseudoLogical(sentId)
	#print "\n===END==="

outF.write(htmlEnd)

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

new = False

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

if new:
	db = client['law_db']
	db_ent = db.semantic_sent_temp
else:
	db = client['tree2relations']
	db_ent = db.entities

db_rel = db.relations

outF = open('/var/www/html/out.html', "w")
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
    for _entity in db_ent.find({'sentenceID':ObjectId(obj_id)}):
	#for _entity in db_ent.find():
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
			
			
def replaceFuncToHtml(text):
	text = text.replace('or', '&or;')
	text = text.replace('and', '&and;')
	text = text.replace('not', '&not;')
	text = text.replace('(IMPL)', '&rArr;')
	text = text.replace('(CIMPL)', '&lArr;')
	return text
		
def getSentencesArraySplitByDot(sent_obj_id):
	sents = []
	
	if new:
		db_entries = db_ent.find({'sentenceID':sent_obj_id})
	else:
		db_entries = db_ent.find({'sentenceID':ObjectId(sent_obj_id)})
	
	curSent = []
	for _entity in db_entries:
		if not _entity['text']:
			continue
			
		if new:
			text = ' '.join(_entity['text'])
		else:
			text = ' '.join(_entity['text'])
			
		#print text
		entityType = _entity['entityType']
		
		curSent.append([text, entityType])
		
		if text == '.':
			sents.append(curSent)
			curSent = []
		
	if len(curSent) > 0:
		sents.append(curSent)
	
	return sents	
	
def ifToLogical(sents):
	sentsOut = []
	ifInBeginning = False

	for sent in sents:
		entities = []
		for _entity in sent:
			text = _entity[0]
			entityType = _entity[1]
			
			if '.' in text: # Finished sentence
				# reset flags
				ifInBeginning = False

			
			if entityType == 'Func':
				if text == 'If': #if in the beginning of the sent
					ifInBeginning = True
					continue # remove if in the beginning
				elif 'if' in text: #if within the sent
					_entity[0] = '(CIMPL)'
				
				if ifInBeginning:
					if text == 'then':
						_entity[0] = '(IMPL)'
				# TODO: if not: search for first komma followed by unary predicate and place then there
		
			entities.append(_entity)
		sentsOut.append(entities)
	return sentsOut
	
	
def implDotFinder(entities):
	implPositions = []
	dotPositions = []

	i = 0
	for _entity in entities:
		text = _entity[0]
		entityType = _entity[1]
		
		# search for (IMPL) and (CIMPL)
		if '(IMPL)' in text or '(CIMPL)' in text:
			implPositions.append(i)
		elif '.' in text:
			dotPositions.append(i)
			
		i = i + 1
		
	return (implPositions, dotPositions)
	
def splitByDotsArray(dotPositions):
	for dotPos in dotPositions:
		if i < dotPos: # Within a sent
			for implPos in implPositions:
				return implPos < dotPos
	return False
	
def bracketSetter(sents):
	sentsOut = []
	
	for sent in sents:
		positions = implDotFinder(sent)
		implPositions = positions[0]
		dotPositions = positions[1]
		
		print implPositions
		
		# TODO: add support for multiple sentences that are finished with dots
	
		#Check if there is a implication within the current sent
		if len(implPositions) == 0 or len(dotPositions) == 0: 
			sentsOut.append(sent) # no implications found, we dont have to fix anything
	
		i = 0
		entitiesOut = []
		for _entity in sent: 
			text = _entity[0]
			entityType = _entity[1]
			
			# start		
			if i == 0:
				entitiesOut.append(['[','Func'])
				
			# front
			if i in implPositions:
				entitiesOut.append([']','Func'])
				
			# back
			if (i-1) in implPositions:
				entitiesOut.append(['[','Func'])
			
			entitiesOut.append(_entity)
			
			#end
			if (i) in dotPositions:
				entitiesOut.append([']','Func'])
				
			i = i + 1
		
		sentsOut.append(entitiesOut)
		
	return sentsOut
		
#5695767ea18bdf03db403463 If sent in beginning
#5695767ea18bdf03db4035b7 if within sent
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
	#for _entity in bracketSetter(ifToLogical(getSentEntitiesArray(sent_obj_id))):
	for sent in bracketSetter(ifToLogical(getSentencesArraySplitByDot(sent_obj_id))):
		for _entity in sent:
			text = _entity[0]
			entityType = _entity[1]
				
			if entityType == "Unary":
				outputText = outputText + green + 'U' + str(uId) + '(' + text + ')' + black + ' & '
				outF.write('<span class="entity" id="' + entityType + '">' + 'U' + str(uId) + '(' + text + ')' + '</span>')
				uId = uId + 1
			elif entityType == "Binary":
				outputText = outputText + red + 'B' + '(' + 'U' + str(uId - 1) + ',' + 'U' +  str(uId) + ')' + text + black + ' & '
				outF.write('<span class="entity" id="' + entityType + '">' +  'B' + '(' + 'U' + str(uId - 1) + ',' + 'U' +  str(uId) + ')' + text + '</span>')
			elif entityType == 'Func' or entityType == 'FuncU':
				label = text
				outputText = outputText + yellow + label + '(' + str(text) + ')' + black + ' '	
				outF.write('<span class="entity" id="' + entityType + '">' + replaceFuncToHtml(text) + '</span>')


	#print outputText[:-2]
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
for sentGroups in list(db_ent.aggregate(pipeline)):

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

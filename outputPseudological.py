import glob
import os

from database import schema
from pymongo import MongoClient

from bson.objectid import ObjectId

from judge.pseudological import *

#define colors
red = "\x1b[31m"
black = "\x1b[0m"
green = "\x1b[32m"
yellow = "\x1b[33m"
yellow2 = "\x1b[4m"

new = True

htmlHead = """{% extends "template.html" %}{% block body %}"""
htmlEnd = """{% endblock %}"""
sentenceDiv = '<div class="sentence">'
divEnd = '</div>'

entColors = [('Binary', red), ('Unary', green), ('Func', yellow), ('FuncU', yellow)]

client = MongoClient()
client = MongoClient('localhost', 27017)

if new:
	db = client['law_db']
	db_ent = db.semantic_sent
else:
	db = client['semantic_sent']
	db_ent = db.entities

db_laws = db.laws
	
outF = open('./templates/pseudological.html', "w")
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
		#   print _entity['lawID']
				
			
def getSent(sent_id):
	sent = db_laws.find_one({'_id': ObjectId(sent_id)})
	return sent
			
def getLaw(law_id):
	law = db_laws.find_one({'_id': ObjectId(law_id)})
	return law
			
#5695767ea18bdf03db403463 If sent in beginning
#5695767ea18bdf03db4035b7 if within sent
def printAndSavePseudoLogical(sent_obj_id):
	outputText = ""
	htmlText = ""
	uId = 0
	bId = 0

	sentObj = getSent(sent_obj_id)
	law = getLaw(sentObj["lawID"])
	
	lawNum = str(law["num"].replace(u'\ufeff', ''))
	law_obj_id = str(law["_id"])
	sentNum = str(sentObj["num"])
	if not sentNum:
		sentNum = "-"
	sentType = str(sentObj["sentType"])
	
	outF.write('<div class="sentence">')
	outF.write('<span id="sentIdentifier">LawNum: ' + lawNum + '/' + sentNum + ' SentType: ' + sentType + ' (LawID:' + law_obj_id + ' SentenceID:' + str(sent_obj_id) + ')</span>')
	outF.write('<p>')
	#for _entity in bracketSetter(ifToLogical(getSentEntitiesArray(sent_obj_id))):
	for sent in filterSents(db_ent, sent_obj_id):
		#outF.write('<span class="entity" id="Func">[</span>')
		
		for _entity in sent:
			text = _entity[0].replace(' ', '_')
			entityType = _entity[1]
				
			if entityType == "Unary":
				outputText = outputText + green + text + '(' + 'x' + str(uId) + ')' + black + ' & '
				outF.write('<span class="entity" id="' + entityType + '">' + text + '(' + 'x' + str(uId) + ')' + '</span>')
				uId = uId + 1
			elif entityType == "Binary":
				outputText = outputText + red + text + '(' + 'e' + str(bId) + ',' + 'x' + str(uId - 1) + ',' + 'x' +  str(uId) + ')' + black + ' & '
				outF.write('<span class="entity" id="' + entityType + '">' + text + '(' + 'e' + str(bId) + ',' + 'x' + str(uId - 1) + ',' + 'x' +  str(uId) + ')' + '</span>')
				bId = bId + 1
			elif entityType == 'Func' or entityType == 'FuncU':
				label = text
				outputText = outputText + yellow + label + '(' + str(text) + ')' + black + ' '  
				outF.write('<span class="entity" id="' + entityType + '">' + replaceFuncToHtml(text) + '</span>')
			else:
				outF.write('<span class="entity" id="' + entityType + '">' + text + '</span>')
		#outF.write('<span class="entity" id="Func">]</span>')

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
ctr = 0
for sentGroups in list(db_ent.aggregate(pipeline)):
	ctr = ctr + 1
	sentId = sentGroups['_id']
	#sentId = '56a20259a18bdf3fadda8eef'

	# sentTxtObj = findSent(sentId)
	# print "LOL", sentTxtObj, sentId
	# continue
	# lawId = sentTxtObj['lawID']
	# sentNum = sentTxtObj['num']
	# sentType = sentTxtObj['sentType']

	print "\n===START==="
	#printSent(sentId)
	#print "\n==="
	#printLegend()
	#print "\n==="
	printAndSavePseudoLogical(sentId)
	print "\n===END==="

outF.write(htmlEnd)
print ctr

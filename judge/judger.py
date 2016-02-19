#!/usr/bin/env python
# coding: utf8

from __future__ import absolute_import
#~ from schema import *
from pymongo import MongoClient
from bson.objectid import ObjectId
from finder_client import get_relavent_laws, get_similarity
from pseudological import filterSents, textFuncFinder

red = "\x1b[31m"
black = "\x1b[0m"
green = "\x1b[32m"
yellow = "\x1b[33m"
yellow2 = "\x1b[4m"

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['law_db']
db_laws = db.laws
db_ent = db.semantic_sent

debug = True
	
def checkCaseInput(case):
	if len(case['Persons']) != 1:
		print "Unsupported person amount! At least for now..."
		return False
	
	if len(case['Act']) == 0:
		print "No input act given..."
		return False
		
	return True
		
def getLawNum(law_id):
	law = db_laws.find_one({'_id': ObjectId(law_id)})
	return law["num"]
		
def getRelevantLaws(case):
	act = case["Act"]
	server_out = get_relavent_laws(act)
	#TODO! Better usage of matched and relavent laws
	#print server_out
	relevantLawIDs = server_out
	#~ relevantLawIDs = case["relevantLawIDs"]
	
	relLawSents = []
	for lawID in relevantLawIDs:
		sents = db_laws.find({'lawID': ObjectId(lawID)})
		
		if sents:
			for relLawSent in sents:
				sentID = relLawSent['_id']
				lawNum = getLawNum(lawID)
				
				entities = db.semantic_sent.find({'sentenceID': str(sentID)})# no ObjectId!
				
				relLawEnts = [(ent['text'], ent['entityType']) for ent in entities] 
				
				logicalSents = filterSents(db_ent, str(sentID))
				relLawSents.append([sentID, relLawSent, relLawEnts, logicalSents, lawNum])
	
	return relLawSents

def similarityCheck(actText, entText):
	# TODO: Implement word2vec similarity check with threshold similarity value?
	similarity = 0
	count = 0
	for actWord in actText.split(" "):
		for entWord in entText.split(" "):
			try:
				sim = float(get_similarity(actWord, entWord))
			except Exception,e:
				print actText, "---", entText, e
			if sim < 0.6:
				continue
			#print entWord, actWord, sim
			similarity += sim
			count += 1
			
	threshold = 0.5 
	
	score = 0
	if similarity > 0:
		score = similarity / count
		out = score >= threshold 
	else:
		out = False

	if debug:
		if out:
			print green, "Entity", entText, "matches action:", "Score:", score, actText, black
		else:
			print green, "Entity", entText, "not matches action:", actText, "Score:", score, black	
	return out
	
def personCheck(persons, entText):
	# TODO: Integrate different persons!
	if entText == "Whoever" and "Bob" in persons:
		if debug:
			print green, "Entity", entText, "matches Bob as person!", black
		return (True, "Bob")
	return (False, "")
	
#TODO: add support for multiple sentences
def splitPremiseResult(logicalSents):
	# eval(B0A,U1, B1B, U2) :- (B0A, U1,D)


	outputPremiseResult = []
	for logicalSent in logicalSents:

		if ["shall", "Func"] in logicalSent:
			# TODO: Define this rule way more abstract
			
			#get position of shall
			posShall = 0
			for i, j in enumerate(logicalSent):
				if j[0] == "shall":
					posShall = i
					
			# strip of result and output tuple (premise, result)
			posShalls = textFuncFinder(logicalSent, "shall", "Func")
			#print "shallPos", shallPos
			
			posBrackets = textFuncFinder(logicalSent, "[", "Func")
			#print "posBracket", posBracket

			if len(posShalls) != 1:
				continue

			posBeginPremise = 0
			for i in reversed(range(posShalls[0], 0)):
				if(i < posShalls[0] and logicalSent[i][0] == "["):
					posBeginPremise = i

			premise = logicalSent[posBeginPremise + 1 : posShalls[0]]

			posEndResult = 0
			for i in range(posShalls[0], len(logicalSent)):
				if(i > posShalls[0] and logicalSent[i][0] == "]"):
					posEndResult = i

			result = logicalSent[posShalls[0] + 1: posEndResult]
			
			outputPremiseResult.append((premise, result))
			
			
		elif ["(IMPL)", "Func"] in logicalSent:
			continue # TODO
		elif ["(RIMPL)", "Func"] in logicalSent:
			continue # TODO
			
	return outputPremiseResult

def premiseToEvalString(premise):
	outputStr = []
	nonFuncCtr = 0
	for i, ent in enumerate(premise):
		entText = ent[0]
		entType = ent[1]
		
		add = ""
		if entType == "Func":
			if entText == "[" or entText == "[f" or entText == "[u":
				if len(outputStr) > 0 and (outputStr[-1][0] == ")" or outputStr[-1][0] == "E"):
					outputStr.append("and") # join a 'and' between opening brackets
				outputStr.append("(")
			elif entText == "]" or entText == "f]" or entText == "[u":
				outputStr.append(")")
			elif entText == "and":
				outputStr.append("and")
			elif entText == "or":
				outputStr.append("or")
		else:
			if entType != "IN" and entType != "Ignore" and entType != "To" and entType != "PREP": # ignore IN tags for evaluation
				#add = entText.replace(' ', '_')
				if len(outputStr) > 0 and (outputStr[-1][0] == ")" or outputStr[-1][0] == "E"):
					outputStr.append("and") # join a 'and' between entities with no func	
				outputStr.append('E' + '[' + str(nonFuncCtr) + ']')
			
			nonFuncCtr += 1
		
	return ' '.join(outputStr)
	
def verifiyLaws(case, laws):
	applicableLaws = []
	for sent in laws:
		
		sentID = sent[0]
		lawSent = sent[1]
		lawEnts = sent[2]
		logicalFormulas = sent[3]
		lawNum = sent[4]
		
		text = lawSent['text']
		actions = case["Action"]
		bobActions = actions["Bob"]
		
		premiseResultFormulas = splitPremiseResult(logicalFormulas)
		
		print "Checking", "SentID", sentID
		
		# Check if we have a Whoever sentence and action based on an actor (Bob)
		if not 'Whoever' in text or not "Bob" in actions:
			if debug:
				print red, 'Unsupported law:', black, sentID
			continue

		for (premise, result) in premiseResultFormulas:
			
			print "Evaluating premise:", premise
			
			truthTable = []
			matchTable = []

			for ent in premise:
				entText = ent[0]
				entType = ent[1]
			
				if entType == "Func":
					continue
			
				done = False
				for act in bobActions:
					#print "Checking entity", ent, "against action:", act

					if (entType == "Unary" or entType == "Binary" or entType == "ADV"):
						personMatch, person = personCheck(case["Persons"], entText)
						
						if personMatch:
							truthTable.append((entText, True))
							matchTable.append((person, entText))
							done = True
							break
						elif similarityCheck(act, entText):
							truthTable.append((entText, True))
							matchTable.append((act, entText))
							done = True
							break
				
				if not done:
					#print "nomatch", entText
					truthTable.append((entText, False))
			
			premiseEval = premiseToEvalString(premise)

			print "TruthTable:", truthTable
			E = [val for (txt, val) in truthTable] # setting up eval variables

			print yellow, "Premise boolean formula:", premiseEval, black
			try:
				evalResult = eval(premiseEval)
			except SyntaxError:
				print "Eval error!"
				evalResult = False
			
			if evalResult:
				resultSent = ' '.join([a for (a,b) in result])
				print red, "Evaluation result: Bob is responsible according to §", lawNum, "and the following should apply:"
				print "\"", resultSent, "\"", black
			else:
				print red, "No matches found. Bob may not responsible according to §", lawNum, black
			
			if evalResult:
				applicableLaws.append([lawNum, resultSent, truthTable, matchTable])
				
	return applicableLaws
	
def run(case):
	if checkCaseInput(case):
		relLaws = getRelevantLaws(case)
		applicableLaws = verifiyLaws(case, relLaws)
		
		# Finally print the whole law check
		for i in range(4):
			print "-------------------------------------------------------------"
		print "Final result:"
		
		if len(applicableLaws) == 0:
			print "No matching laws found. Sorry..."
			return
		
		for i, [lawNum, result, truthTable, matchTable] in enumerate(applicableLaws):
			print str(i+1) + ".", red, '§' + str(lawNum), "applies and the following should apply:", result , black
			
			print yellow, "Facts:", black
			for act, entText in matchTable:
					print act, "=>", entText
		
if __name__ == "__main__":
	# Bob hits John several times. John suffers thereby a laceration on his head, which is associated with severe pain. Bob just wanted explicit to injure John with the beatings.

	#works
	#RelevantLaw: 167a
	#case = { "Persons" : ["Bob"], 
	#		"Action": {	"Bob" : ["knowingly", "interrupts", "a burial"]}, 
	#		"Act" : "Bob knowingly interrupts a burial"}

	#works (no match should be found)
	#case = { "Persons" : ["Bob"], 
	#		"Action": {	"Bob" : ["unknowingly", "interrupts", "a burial"]}, 
	#		"Act" : "Bob unknowingly interrupts a burial"}
	
	#works
	#RelevantLaw: 222
	#case = { "Persons" : ["Bob"], 
	#	"Action": {	"Bob" : ["killed", "a human", "carelessness"]}, 
	#	"Act" : "Bob killed a human by carelessness"}
	
	#works
	#case = { "Persons" : ["Bob"], 
	#	"Action": {	"Bob" : ["ridicules", "memory of a deceased person"]}, 
	#	"Act" : "Bob ridicules a memory of a deceased person"}
	
	run(case)
	#similarityCheck("death of a human being", "death of a human being")

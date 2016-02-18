import nltk
import re
import glob
import os

from database.schema import *

#define colors
red = "\x1b[31m"
black = "\x1b[0m"
green = "\x1b[32m"
yellow = "\x1b[33m"
yellow2 = "\x1b[4m"


from database.schema import *
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['law_db']
laws_db = db.laws

def getParentSent(parentID):
	return laws_db.find_one({'_id':parentID})

def checkIfSentIsParent(sentID):
	return laws_db.find_one({'parentSentID' : str(sentID)}) != None
	
def filterParentText(txt):
	# Remove : signs at the end
	#rex = re.search('^.*(?=:)', txt)
	#if rex:
		#txt = rex.group(0)
		
	return txt
	
def filterSubText(txt):
	# Remove "; or" at the end
	rex = re.search('^.*(?=; or)', txt)
	if rex:
		txt = rex.group(0)
		
	return txt
	
def filterSubSubText(txt):
	return txt
	
# not working: 14
for laws in laws_db.find({'num': '11'}):
	if 'title' in laws:
		print(laws['title'])
		law_id = laws['_id']
		print law_id
		
		if checkIfSentIsParent(law_id):
			print "Skipping", law_id
			continue
		
		for sent in laws_db.find({'lawID': law_id}):
			sentType = sent["sentType"]
			text = sent['text']

			print green, "Type:", sentType, "Parent:", sent["parentSentID"], "Sent:", text, black
			
			if sentType == SentTypes.SubSent:
				# Join together with previous sent
				
				text = filterSubText(text)
				
				parentID = sent["parentSentID"]
				parentText = filterParentText(getParentSent(parentID)['text'])
				
				joinedSent = parentText + " " + text

				print red, "Joined:", joinedSent, black
			elif sentType == SentTypes.SubSubSent:
				# Join subsubsent together with previous sents
				
				text = filterSubSubText(text)
				
				parentID = sent["parentSentID"]
				parentSent = getParentSent(parentID)
				parentText = filterSubText(parentSent['text'])
				
				parentParentID = parentSent["parentSentID"]
				parentParentText = filterParentText(getParentSent(parentParentID)['text'])

				joinedSent = parentParentText + " " + parentText + " " + text

				print red, "Joined:", joinedSent, black
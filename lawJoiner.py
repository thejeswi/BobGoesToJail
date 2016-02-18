import nltk
import re
import glob
import os

from database.schema import *
from bson.objectid import ObjectId

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

def getSentsByParent(parentID):
	return laws_db.find({'parentSentID' : ObjectId(parentID)})
	
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
	
# special: 11
# not working: 14
for laws in laws_db.find({'num': '5'}):
	if 'title' in laws:
		law_id = laws['_id']
		print "Processing law:", laws['title'], law_id
		

		for sent in laws_db.find({'lawID': law_id}):
			sentType = sent["sentType"]
			text = sent['text']
						
			if sentType != SentTypes.BeginSent and sentType != SentTypes.NumberSent:
				print "Skipping non parent sent:", sent['_id'], sentType
				continue
			
			print "[MAIN", text, "MAIN]"
			subSents = getSentsByParent(sent['_id'])
			
			print "[SUBS"
			
			# get subsubsents
			for subSent in subSents:
				subSubSents = getSentsByParent(subSent['_id'])
				subSubSentsTxtLst = [str(subSubSent['text']) for subSubSent in subSubSents]
				
				subsubtxt = ""
				if len(subSubSentsTxtLst) > 0:
					subsubtxt += "[SUBSUBS "
					for subsubSentTxt in subSubSentsTxtLst:
						subsubtxt += "[SUBSUB " + subsubSentTxt + " SUBSUB]"
					subsubtxt += " SUBSUBS]"
					
				print red, "[SUB", subSent['text'], green, subsubtxt, red, "SUB]", black
				
			print "SUBS]"
				
			
			#outSents[text].append(subElements)
	
		#joinSubsents(outSents)

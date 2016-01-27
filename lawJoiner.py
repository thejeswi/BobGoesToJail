import nltk
import re
import glob
import os

from database.schema import *

#define colors
red = "\x1b[31m"
black = "\x1b[0m"
grey = "\x1b[30m"


from database.schema import *
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['law_db']
laws_db = db.laws

def getParentSent(parentID):
	return laws_db.find_one({'_id':parentID})

for laws in laws_db.find({'num': '7'}):
    if 'title' in laws:
        print(laws['title'])
        law_id = laws['_id']
        print law_id
        
        print "Sents:"
        for sent in laws_db.find({'lawID': law_id}):
            sentType = sent["sentType"]

	    if sentType == SentTypes.SubSent:
		
		#print sent
		subText = sent['text']

		# Join together with previous sent
		parentID = sent["parentSentID"]
		parentText = getParentSent(parentID)['text']

		# Remove : signs
		print re.search('(.+?):', parentText).group(0)

		joinedSent = parentText + subText

		print joinedSent

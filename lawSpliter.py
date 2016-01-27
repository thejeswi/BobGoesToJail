import nltk
import re
import glob
import os

#define colors
red = "\x1b[31m"
black = "\x1b[0m"
grey = "\x1b[30m"

def parseLaw(lawTxt):

    # title, {law, subsection, sentence}
    splLines = lawTxt.split('\n')

    infoLine = splLines[0].split(' ')
    lawNum = infoLine[0]
    lawTitle = splLines[0][len(lawNum) + 1:]

    myLaw = law()
    myLaw.num = lawNum
    myLaw.title = lawTitle

    lawID = laws_db.insert_one(myLaw.out()).inserted_id
    print "Stored Law:", lawNum, "ID:", lawID


    lawLines = splLines[1:]

    state = 0
    beginSent = ""
    previousSubSents = []

    sentences = {}

    previousSent = ""
    nonFinishedSent = False

    parentID = None
    subParentID = None

    def storeSent(laws_db, lawID, text, num, sentType, parentID):
        mySent = sentence()
        mySent.num = num
        mySent.text = text
        mySent.sentType = sentType
        mySent.lawID = lawID
        mySent.parentSentID = parentID
	print red, mySent.parentSentID, black
        return laws_db.insert_one(mySent.out()).inserted_id

    for line in lawLines:
	
        if len(line) == 0 or re.search(r"^ *$", line):
            continue

        print "Inp:" , line

        #################################################
        # Re-union non finished sentences
        if nonFinishedSent:
            nonFinishedSent = False
            line = previousSent + line
            print red, line, black
        #################################################

        if re.search(r"^[A-Z](.*?)\.$", line):
            normalSent = line
            state = 0

            num = ""
            myParentID = 0
            parentID = storeSent(laws_db, lawID, normalSent, num, SentTypes.NormalSent, myParentID)

            print red, "NormalSent", black, normalSent, parentID

            if re.search(r',$',line) or re.search(r'[a-zA-Z]$',line):
                print red, "Found non finished sentence", black
                previousSent = line
                nonFinishedSent = True

            continue

        ################################################# 
        # Sentences which may have subsentences
        #################################################
        elif re.search(r"^\([0-9]+\)[a-zA-Z\s,;\.]*", line):
            bracketIdx = line.find(')')
            numberSent = line[bracketIdx + 2:]
            state = 1

            num = re.findall("\((.*?)\)", line)[0]
            myParentID = 0
            parentID = storeSent(laws_db, lawID, numberSent, num, SentTypes.NumberSent, myParentID)

            print red, "NumberSent", black, numberSent, parentID, num

            if re.search(r',$',line) or re.search(r'[a-zA-Z]$',line):
                print red, "Found non finished sentence", black
                previousSent = line
                nonFinishedSent = True

            continue
        elif re.search(r"^[a-zA-Z\s]*\.", line):
            endSent = line

            num = ""
            storeSent(laws_db, lawID, endSent, num, SentTypes.EndSent, parentID)

            print red, "EndSent", black, endSent

            continue
        #################################################
        # law regex: e.g. (1) If someone acts:   OR  Should be applied to: #rem \([0-9]+\)
        #re.search(r"\([0-9]+\)[a-zA-Z\s]:$", line) or 
        #################################################
        elif re.search(r"^[A-Z](.*?):$", line): 
            state = 1
            beginSent = line
            previousSents = []

            brackets = re.findall("\((.*?)\)", line)

            num = ""
            if len(brackets) > 0:
                num = brackets[0]

            parentID = storeSent(laws_db, lawID, beginSent, num, SentTypes.BeginSent, parentID)
            print red, "BeginSent", black, beginSent, parentID, num

            continue
        if state == 1 or state == 2:
            if re.search(r"^\s*[0-9]+[a-z]?\.", line):
                pointIdx = line.find('.')

                subSent = line[pointIdx + 2:]

                state = 2
                previousSubSents.append(subSent)

                num = re.findall("(.*?)\.", line)[0]
                subParentID = storeSent(laws_db, lawID, subSent, num, SentTypes.SubSent, parentID)
		
                print red, "SubSent", black, subSent, subParentID, parentID, num

                continue
            elif state == 2 and re.search(r"^\([a-z]\)", line):
                bracketIdx = line.find(')')
                subsubsent = line[bracketIdx + 2:]
                state = 2
                previousSubSents.append(subsubsent)

                num = re.findall("\((.*?)\)", line)[0]
                storeSent(laws_db, lawID, subsubsent, num, SentTypes.SubSubSent, subParentID)

                print red, "SubSubSent:", black, subsubsent, num

                continue
            elif re.search(r"^[a-zA-Z\s]*\.", line):
                # end of sent
                endSent = line
                state = 0
                subParentID = None

                num = ""
                storeSent(laws_db, lawID, endSent, num, SentTypes.EndSent, subParentID)
                #print "end:", endSent
        #################################################
                #for subSent in previousSubSents:
                #    print "Prev:", beginSent, subSent, endSent
        else:
            print red, "Unrecognized sentence/line:", line, black
                

from database.schema import *
from pymongo import MongoClient

path = '/home/mlc/BobGoesToJail/corpus/lawTexts_en'

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['law_db']
laws_db = db.laws

for filename in glob.glob(os.path.join(path, '*.txt')):
    print filename
    fTxt = open(filename)
    #fTxt = open(path + "/109k.txt")
    parseLaw(fTxt.read())   
    fTxt.close()   

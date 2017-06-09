import sys
from pymongo import MongoClient
from re import match
import heapq
import requests

ignoreWords = ["a", "in", "and", "be", "non", "the"]

def synListGen():
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client['law_db']
    synLists = db.entity_synonyms.find()
    for syns in synLists:
        sWords = syns["synonyms"]
        if len(sWords) == 0:
            continue
        if sWords == [None]:
            continue
        if sWords[0] == None:
            continue
        for sWordList in sWords:
            if sWordList == None:
                continue
            for sWord in sWordList:
                if sWord.lower() in ignoreWords:
                    continue
                if len(sWord) < 3:
                    continue
                yield (str(sWord), syns["sentenceID"])
    
def law_matcher(model, inputCase):
    #~ inputCase = "Bob wanted explicitly the injure John with the use of melee Weapons"
    #~ inputCase = "funeral"
    caseWords = inputCase.split(" ")
    relaventLaws = dict()
    wordCount = dict()
    matchedLaws = []
    for sWord in synListGen():
        sentID = sWord[1]
        sWord = sWord[0].lower()
        for cWord in caseWords:
            cWord = cWord.lower()
            try: similarity = model.similarity(cWord, sWord)
            #~ try: similarity = float(requests.get('http://127.0.0.1:9090/'+cWord+"/"+sWord).text)
            #Word to vector fails if word is not present in corpus
            except Exception,e: similarity = 0
            if similarity > 0.999999:
                matchedLaws.append(sentID)
            if similarity > 0.5:
                if sentID not in relaventLaws:
                    #~ print "Matched", cWord, sWord
                    relaventLaws[sentID] = 0
                    wordCount[sentID] = 0
                relaventLaws[sentID] += similarity
                wordCount[sentID] += 1 
    #Normalization
    for key, value in relaventLaws.iteritems():
        relaventLaws[key] = relaventLaws[key].astype(float) / wordCount[key]
    from pprint import pprint
    pprint({"match":list(set(matchedLaws)), "rel":relaventLaws})
    return {"match":list(set(matchedLaws)), "rel":relaventLaws}

if __name__ == "__main__":
    print law_matcher()

import sys
from pymongo import MongoClient
from bson.objectid import ObjectId
from re import match
import heapq
import requests
from synList import synList
ignoreWords = ["a", "in", "and", "be", "non", "the"]

#~ def similarity_finder(model, word1, word2):
    #~ try: similarity = model.similarity(word1, word2)
    #~ except Exception,e: similarity = 0
    #~ return similarity

def similarity_finder(model, word1, word2):
    synWord1 = synList(word1)
    synWord2 = synList(word2)
    s = []
    for w1 in synWord1:
        for w2 in synWord2:
            try: s.append(model.similarity(w1, w2))
            except Exception,e: s.append(0.0)
    if s == []:
        return 0
    return max(s)

#~ def entity_matcher(model, inputPhrase, sentenceID):
    #~ caseWords = inputPhrase.split(" ")
    #~ relaventEnts = dict()
    #~ wordCount = dict()
    #~ matchedEnts = []
    #~ for entityDict in synListGen(sentenceID):
        #~ entID = entityDict["entityID"]
        #~ sWords = entityDict["syns"]
        #~ for sWord in sWords:
            #~ for cWord in caseWords:
                #~ cWord = cWord.lower()
                #~ try: similarity = model.similarity(cWord, sWord)
                #~ #Word to vector fails if word is not present in corpus
                #~ except Exception,e: similarity = 0
                #~ if similarity > 0.9999:
                    #~ matchedEnts.append(entID)
                #~ if similarity > 0.5:
                    #~ if entID not in relaventEnts:
                        #~ print cWord, sWord
                        #~ relaventEnts[entID] = 0
                        #~ wordCount[entID] = 0
                    #~ relaventEnts[entID] += similarity
                    #~ wordCount[entID] += 1
    #~ #Normalization
    #~ for key, value in relaventEnts.iteritems():
        #~ relaventEnts[key] = relaventEnts[key].astype(float) / wordCount[key]
    #~ return {"match":list(set(matchedEnts)), "rel":relaventEnts}

if __name__ == "__main__":
    #~ print law_matcher()
    #~ synListGen("56a20259a18bdf3fadda90a8")
    for s in synListGen("56a20259a18bdf3fadda90a8"):
        print s

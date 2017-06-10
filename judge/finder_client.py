from pymongo import MongoClient
import requests
from bson.objectid import ObjectId
import operator
import json

url = "http://127.0.0.1:9090/"

client = MongoClient('localhost', 27017)
db = client['law_db']

def get_relavent_laws(case):
    "Example output: [ObjectId('5939af52608f062057d0d1b8'), "
    "               ObjectId('5939af52608f062057d0d156'),"
    "               ObjectId('5939af51608f062057d0cd7a')]"
    res = requests.get(url+"law/"+str(case)).text
    #~ #Example return of server:
    #~ {'rel': {u'56a20258a18bdf3fadda8bfb': 0.90552999998256434, u'56a20258a18bdf3fadda8e52': 1.0000000000000009, u'56a20255a18bdf3fadda8054': 1.0000000000000009}, 'match': [u'56a20258a18bdf3fadda8bfb', u'56a20258a18bdf3fadda8e52', u'56a20255a18bdf3fadda8054']}
    
    # Replace mechanism! This is dangerous
    exec "res="+res
    
    #Suggested mechanism below: It fails because the value will not be a string
    #json.loads accepts only single quotes
    #~ res = res.replace("'",'"')
    #~ print res
    #~ res = json.loads(res)
    
    rel = res["rel"]
    sorted_rel = sorted(rel.items(), key=operator.itemgetter(1), reverse = True)

    #Current method of taking the five best matches
    lawsList = sorted_rel[:5]
    
    toSend = []
    for sentID in lawsList:
        toSend.append(db.laws.find_one({"_id":ObjectId(sentID[0])})["lawID"])
    
    #Old method for the matching
    #~ for sentID in res["match"]:
        #~ if res["rel"][sentID] > 0.85: #~~~~~~~~~~ This was 0.7 before!
            #~ lawsList.append(db.laws.find_one({"_id":ObjectId(sentID)})["lawID"])
    
   
    return list(set(toSend))

def get_similarity(word1, word2):
    word1 = word1.replace(" ","_")
    word2 = word2.replace(" ","_")
    finalURL = url+"ent/"+str(word1)+"/"+str(word2)
    if word1.strip() == "" or word2.strip() == "":
        return "0.0"
    #~ print "Requesting server:", finalURL
    res = requests.get(finalURL).text
    return res
    
if __name__ == "__main__":
    #~ print get_relavent_laws("Bob disturbs a funeral service")
    print get_similarity("instrument","guitar")
    #~ print get_matched_entities("disturbs a funeral service", "56a20258a18bdf3fadda8bfb")['match']
    

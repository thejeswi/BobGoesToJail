from pymongo import MongoClient
import requests
from bson.objectid import ObjectId

url = "http://127.0.0.1:9090/"

client = MongoClient('localhost', 27017)
db = client['law_db']

def get_relavent_laws(case):
    res = requests.get(url+"law/"+str(case)).text
    exec "res="+res
    lawsList = []
    for sentID in res["match"]:
        if res["rel"][sentID] > 0.7:
            lawsList.append(db.laws.find_one({"_id":ObjectId(sentID)})["lawID"])
    #Example return of server:
    #~ {'rel': {u'56a20258a18bdf3fadda8bfb': 0.90552999998256434, u'56a20258a18bdf3fadda8e52': 1.0000000000000009, u'56a20255a18bdf3fadda8054': 1.0000000000000009}, 'match': [u'56a20258a18bdf3fadda8bfb', u'56a20258a18bdf3fadda8e52', u'56a20255a18bdf3fadda8054']}
    return list(set(lawsList))

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
    

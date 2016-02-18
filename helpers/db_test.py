from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['raw_law']
laws_db = db.laws

from filters.corpus2DB.schema import raw_law

def insert_law():
    newLaw = raw_law()
    newLaw.num = "15",
    newLaw.title = "Law Title",
    newLaw.text = ["This is a law_text"]
    law_id = laws_db.insert_one(newLaw.out()).inserted_id
    print law_id

def find_law():
    found_law = laws_db.find_one({"num":"15"})
    print found_law
    
def find_laws():
    from pprint import pprint
    found_laws = laws_db.find()
    for law in found_laws:
        pprint(law) 


find_laws()

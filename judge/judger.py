from schema import *
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['law_db']
db_laws = db.laws
db_ent = db.entities

# Bob hits John several times. John suffers thereby a laceration on his head, which is associated with severe pain. Bob just wanted explicit to injure John with the beatings.

case = { "Persons" : ["Bob", "John"], 
		"Attributes": {"Bob" : ["hits", "wanted explicit"], 
		"John": ["suffers", "beatings", "laceration on his head"]}, 
		"Act" : "Bob hits John"}
		
# title search
# word search
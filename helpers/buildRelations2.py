import glob
import os

from database.schema import *
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.son import SON

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['tree2relations']

db_rel = db.relations

### Simple relations between neighbouring entities
def buildSimpleRelations(obj_id):
	entityList = []
	for db_entity in db.entities.find({'sentenceID':ObjectId(obj_id)}):
		entType = db_entity['entityType']
		entID = db_entity['_id']
		print 'Building relations for law id', entID
		entityList.append((entType, entID))

	for i in range(len(entityList)):
		entType = entityList[i][0]
		entID = entityList[i][1]

		if entType == 'Binary' or entType == 'Func':

			if (i-1) in range(len(entityList)):
                                previousEntity = entityList[i-1]
				
				# Relation previous->this
				link = entityLink()
				link.EntityFromID = previousEntity[1]
				link.EntityToID = entID
				db_rel.insert_one(link.out())

			if (i+1) in range(len(entityList)):
				nextEntity = entityList[i+1]

				# Relation this->next
				link = entityLink()
				link.EntityFromID = entID
				link.EntityToID = nextEntity[1]
				db_rel.insert_one(link.out())						
			

pipeline = [{"$group": {"_id": "$sentenceID"}}]
for sent in list(db.entities.aggregate(pipeline)):
        buildSimpleRelations(sent['_id'])

import json
import datetime
from enum import Enum


###### Splitted Law Objects ###################

class SentTypes(Enum):
    Undefined = 0
    BeginSent = 1
    NumberSent = 2
    NormalSent = 3
    EndSent = 4
    SubSent = 5
    SubSubSent = 6

class law(object):
    def __init__(self):
        self.num = "Undefined",
        self.title = "Undefined",
        self.time = datetime.datetime.utcnow()
    def out(self):
        return {
                "num" : self.num,
                "title": self.title,
                "time":self.time
                }

class sentence(object):
    def __init__(self):
        self.num = "Undefined",
	self.sentType = SentTypes.Undefined
        self.text = []
	self.lawID = None, # ID of the law
        self.parentSentID = None, #ID of the parentSent
        self.time = datetime.datetime.utcnow()
    def out(self):
        return {
                "num" : self.num,
                "sentType" : self.sentType,
                "text": self.text,
                "lawID": self.lawID,
                "parentSentID": self.parentSentID,
                "time":self.time
                }
###############################################


###### Tree 2 Entity Relations ################


class entity(object):
    def __init__(self):
        self.text = "Undefined",
        self.entityType = "Undefined",
        self.lawID = None
        self.sentenceID = None
        self.time = datetime.datetime.utcnow()
    def out(self):
        return {
                "text" : self.text,
                "entityType": self.entityType,
                "time":self.time,
                "sentenceID":self.sentenceID,
                "time":self.time,
                }

class entityLink(object):
    def __init__(self):
        self.EntityFromID = "Undefined",
        self.EntityToID = "Undefined",
        self.time = datetime.datetime.utcnow()
    def out(self):
        return {
                "EntityFromID": self.EntityFromID,
                "EntityToID": self.EntityToID,
                "time":self.time
                }


###############################################




class annotation(object):
    def __init__(self):
        self.entityType = "Undefined",
        self.lawNum = "Undefined"
	self.start = 0,
        self.end = 0,
	self.phrase = "Undefined",
	self.time = datetime.datetime.utcnow()
    def out(self):
        return {
                "entityType" : self.entityType,
		"lawNum" : self.lawNum,
                "start": self.start,
		"end": self.end,
		"phrase": self.phrase,
                "time": self.time
                }


class subLink_law_pos(object):
    def __init__(self):
        self.num = "Undefined",
        self.pos = []
        self.time = datetime.datetime.utcnow()
    def out(self):
        return {
                "num" : self.num,
                "title": self.title,
                "text": self.text,
                "is_sublaw":self.is_sublaw,
                "super_law":self.super_law,
                "time":self.time
                }


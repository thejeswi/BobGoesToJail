import json
import datetime
from enum import Enum


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

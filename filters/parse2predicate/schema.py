import json
import datetime
from enum import Enum
import re


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
                "time":re.escape(str(self.time)),
                "lawID":re.escape(str(self.lawID)),
                "sentenceID":re.escape(str(self.sentenceID))
                }

class ruledParsedTrees(object):
    def __init__(self):
        self.parseTree = "Undefined",
        self.lawID = None
        self.sentenceID = None
        self.time = datetime.datetime.utcnow()
    def out(self):
        return {
                "parseTree" : self.parseTree,
                "time":self.time,
                "lawID":self.lawID,
                "sentenceID":self.sentenceID,
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


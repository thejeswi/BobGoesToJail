from nltk.corpus import wordnet as wn
import schema
import nltk
import re
import synList
from pprint import pprint
from pymongo import MongoClient


client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['law_db']


def generate(raw_word):
    """Generates a list of synomyns for a given input word"""
    words = wn.synsets(raw_word)
    synList = set()
    for word in words:
        try:
            synList.update(word.lemma_names())
        except:
            synList.update(word.lemma_names)
    return list(synList)

def sentence_input(words):
    for word in words:
        syn = generate(word)
        if syn == []:
            yield None
            continue
        yield syn
        

def filter_unwanted(words):
    for word in words:
        if re.match("[0-9].*",word):
            continue
        if re.match("^-[A-Z].*-$",word):
            continue
        yield word

def synList():
    entities = db.semantic_sent.find()
    #~ entities = db.semantic_sent.find()
    for entity in entities:
        sent = entity['text']
        filterWords = filter_unwanted(sent)
        synonyms = sentence_input(filterWords)
        syns = schema.synonyms()
        syns.sentenceID = entity['sentenceID']
        syns.entityID = entity['_id']
        syns.synonyms = [x for x in synonyms]
        print syns.out(), "\n#########################"
        db.entity_synonyms.insert_one(syns.out())

if __name__ == "__main__":
    db.entity_synonyms.drop()
    synList()
    #~ print "Enter a sentence"
    #~ listofWords = raw_input().split()
    #~ superSynSet = []
    #~ for word in listofWords:
        #~ superSynSet = superSynSet + generate(word)
    #~ pprint(superSynSet)


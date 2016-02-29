from nltk.corpus import wordnet as wn
import nltk
import re
import synList
from pprint import pprint
from pymongo import MongoClient


client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['law_db']

word_syns = db.word_synonyms

def generate(raw_word):
    """Generates a list of synomyns for a given input word"""
    syns = db.word_syns.find_one({"word":raw_word.lower()})
    if syns is not None:
        return syns["syns"]
    words = wn.synsets(raw_word)
    synList = set()
    for word in words:
        try:
            synList.update(word.lemma_names())
        except:
            synList.update(word.lemma_names)
    synList = list(synList)
    db.word_syns.insert_one({"word":raw_word, "syns":synList})
    return synList

def synList(words):
    entities = words.split(" ")
    for sent in entities:
        synonyms = generate(sent)
        synonyms = [x for x in synonyms]
        return synonyms

if __name__ == "__main__":
    print synList("penalty")

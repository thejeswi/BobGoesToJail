from nltk.corpus import wordnet as wn
import nltk
from pprint import pprint

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

if __name__ == "__main__":
    print "Enter a sentence"
    listofWords = raw_input().split()
    superSynSet = []
    for word in listofWords:
        superSynSet = superSynSet + generate(word)
    pprint(superSynSet)

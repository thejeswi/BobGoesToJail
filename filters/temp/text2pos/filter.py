import nltk
import json

fTxt = open("/home/mlc/BobGoesToJail/corpus/lawTexts_en/14.txt")
lawTxt = fTxt.read()

lawLines = lawTxt.split("\n")
pos_lawLines = []

for line in lawLines:
    text = nltk.word_tokenize(line)
    posTags = nltk.pos_tag(text)
    pos_lawLines.append(posTags)

print pos_lawLines[0]

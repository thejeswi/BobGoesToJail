import nltk
from pprint import pprint
import re
from traverse import traverse
from stringParser import stringParser
from rules import rules

ignoreWords = ["cause","causes", "the", "a", "to"]

def getWordList(tree, wordList = []):
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree or type(subtree) == nltk.tree.ParentedTree:
            getWordList(subtree, wordList)
        else:
            wordList = wordList.append(subtree)
            #~ print "Else part:", subtree
            break
    if (wordList == None):
        return [str(tree[0])]
    return wordList

def getWordListSimple(tree, wordList = []):
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree or type(subtree) == nltk.tree.ParentedTree:
            getWordList(subtree, wordList)
        else:
            wordList = wordList.append(subtree)
            #~ print "Else part:", subtree
            break
    if (wordList == None):
        return [str(tree[0])]
    return wordList
def removeWP(tree):
    tree = str(tree)
    tree = " ".join(" ".join(tree.split("\n")).split())
    return tree

def groupSplitter(subTreeStr, wordList, toSplitAt):
    funcWord = toSplitAt.group(1).split(")")[0]
    listSub = subTreeStr.split(")")
    splitWords = []
    for sub in listSub:
        sub = sub.strip()
        if sub[0:5] == "(Func":
            splitWords.append(sub[6:])
    locationList = []
    #~ print wordList, "\n******************"
    for spw in splitWords:
        i=0
        for word in wordList:
            if word == spw and not (i  in locationList):
                locationList.append(i)
                #~ print "The word", wordList[i], i
            i += 1
    return locationList

def traverseTree(tree, finalList = []):
    for subtree in tree:
        unaryFlag = False
        if type(subtree) == nltk.tree.Tree:
            label = subtree.label()
            wordList = getWordList(subtree, [])
            if label == "ADV":
                finalList.append(("ADV", wordList))
                continue
            if label == "Func":
                finalList.append(("Func", wordList))
                continue
            if label == "Unary":
                finalList.append(("Unary", wordList))
                continue
            if label == "PREP":
                finalList.append(("PREP", wordList))
                continue
            traverseTree(subtree, finalList)
            if label == "Comma":
                finalList.append(("Comma", ","))
            if label == "Point":
                finalList.append(("Point", "."))
        else:
            #Skip the BInary for . and ,
            #~ if subtree.strip() == "." or subtree.strip() == ",":
                #~ continue
            finalList.append(("Binary", [subtree]))
    return finalList

def sameStuffCombiner(listOfStuff):
    previousTag = None
    finalStuff = []
    for stuff in listOfStuff:
        if stuff[1] == None:
            #~ print stuff[0],"Error found"
            continue
        if stuff[0] == previousTag:
            if stuff[0] == "Func":
                finalStuff.append(stuff)
                previousTag = stuff[0]
                continue
            finalStuff[-1][1].extend(stuff[1])
        else:
            finalStuff.append(stuff)
            previousTag = stuff[0]
    return finalStuff

def treeToString(s):
    tree = nltk.tree.Tree.fromstring(s)
    listOfStuff = traverseTree(tree, [])
    combined = sameStuffCombiner(listOfStuff)
    newCombined = []
    for c in combined:
        if c == ('Binary', ['causes']):
            c = ('Ignore', ['causes'])
        if c == ('Binary', ['to']):
            c = ('To', ['to'])
        newCombined.append(c)
    return newCombined

if __name__ == "__main__":
    s = open("parsedTree.txt", "rU").read()
    print treeToString(s)

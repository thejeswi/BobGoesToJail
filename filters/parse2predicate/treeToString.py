import nltk
from pprint import pprint
import re

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
            if label == "Func":
                #~ print "FuncTree: ",subtree
                finalList.append(("Func", getWordList(subtree, [])))
                continue
            if label == "Unary":
                #~ subTreeStr = removeWP(subtree)
                #~ toSplitAt = re.search("^.*\(Func (.*)\).*$", subTreeStr)
                #~ if toSplitAt:
                    #~ subTree = nltk.ParentedTree.fromstring(subTreeStr)
                    #~ wordList = getWordList(subTree)
                    #~ splitList = groupSplitter(subTreeStr, wordList, toSplitAt)
                    #~ #Something to store seperate stuff
                    #~ lastLoc = 0
                    #~ for split in splitList:
                        #~ #print(("Unary", wordList[lastLoc:split-1]))
                        #~ finalList.append(("UnaryS", wordList[lastLoc:split-1]))
                        #~ #print(("FuncU", [wordList[split]]))
                        #~ finalList.append(("FuncU", [wordList[split]]))
                        #~ lastLoc = split+1
                    #~ #print("Unary",wordList[lastLoc:])
                    #~ finalList.append(("UnaryE",wordList[lastLoc:]))
                    #~ continue
                wordList = getWordList(subtree, [])
                finalList.append(("Unary", wordList))
                continue
            traverseTree(subtree, finalList)
        else:
            #Skip the BInary for . and ,
            if subtree.strip() == "." or subtree.strip() == ",":
                continue
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
            finalStuff[-1][1].extend(stuff[1])
        else:
            finalStuff.append(stuff)
            previousTag = stuff[0]
    return finalStuff

def treeToString(s):
    tree = nltk.tree.Tree.fromstring(s)
    listOfStuff = traverseTree(tree, [])
    combined = sameStuffCombiner(listOfStuff)
    return combined

if __name__ == "__main__":
    s = open("parsedTree.txt", "rU").read()
    print treeToString(s)

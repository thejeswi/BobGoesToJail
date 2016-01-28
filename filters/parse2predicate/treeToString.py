import nltk
s = open("parsedTree.txt", "rU").read()
tree = nltk.tree.Tree.fromstring(s)

def getWordList(tree, wordList = []):
    #print("tree:", tree)
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            getWordList(subtree, wordList)
        else:
            return wordList.append(subtree)
    return wordList


def traverseTree(tree, finalList = []):
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            label = subtree.label()
            if label == "Unary":
                #~ print "Unary: ", getWordList(subtree, [])
                finalList.append(("Unary", getWordList(subtree, [])))
                continue
            if label == "Func":
                #~ print "Func: ", getWordList(subtree, [])
                finalList.append(("Func", getWordList(subtree, [])))
                continue
            traverseTree(subtree, finalList)
        else:
            #~ print "Binary: ", subtree
            finalList.append(("Binary", [subtree]))
    return finalList
    
#~ def sameStuffCombinerOld(listOfStuff):
    #~ correctStuff = []
    #~ lastFirstElemId = None
    #~ previousTag = None
    #~ for i in range(len(listOfStuff) - 1):
        #~ if previousTag != listOfStuff[i][0] and listOfStuff[i][0] == listOfStuff[i+1][0] and lastFirstElemId:
            #~ firstElem = listOfStuff[lastFirstElemId]
            #~ firstElem[1].append(listOfStuff[i+1])
            #~ print 'Adding', listOfStuff[i+1], 'to', firstElem
        #~ else:
            #~ correctStuff.append(listOfStuff[i])
            #~ lastFirstElemId = i
            #~ previousTag = listOfStuff[i][0]
            #~ print 'First', lastFirstElemId, listOfStuff[i]
    #~ return correctStuff
        
def sameStuffCombiner(listOfStuff):
    correctStuff = []
    lastFirstElemId = None
    previousTag = None
    for i in range(len(listOfStuff)):
        if previousTag == listOfStuff[i][0]:
            firstElem = listOfStuff[lastFirstElemId]
            firstElem[1].extend(listOfStuff[i][1])
            #~ print 'Adding', listOfStuff[i][1], 'to', firstElem
        else:
            correctStuff.append(listOfStuff[i])
            lastFirstElemId = i
            previousTag = listOfStuff[i][0]
            #~ print 'First', lastFirstElemId, listOfStuff[i]
    return correctStuff

listOfStuff = traverseTree(tree, [])
#~ print listOfStuff
from pprint import pprint
pprint(sameStuffCombiner(listOfStuff))

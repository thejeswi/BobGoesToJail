import re
from nltk import ParentedTree

parsedSent = """(ROOT (S (NP (NP (NP (NNS Sections)) (NP (CD 30) (NN subsection) (PRN (-LRB- -LRB-) (NP (CD 1)) (-RRB- -RRB-)))) (, ,) (NP (NP (CD 31) (NN subsection) (PRN (-LRB- -LRB-) (NP (CD 1)) (-RRB- -RRB-))) (, ,) (NP (NN no.) (CD 1))) (, ,)) (VP (MD shall) (VP (VB apply) (ADVP (RB accordingly)) (PP (PP (TO to) (NP (NP (VBN attempted) (NN incitement)) (PP (IN of) (NP (NP (JJ false) (JJ unsworn) (NN testimony)) (PRN (-LRB- -LRB-) (NP (NN Section) (CD 153)) (-RRB- -RRB-)))))) (CC and) (PP (IN of) (NP (NP (DT a) (JJ false) (NN affirmation)) (PP (IN in) (NP (NP (NN lieu)) (PP (IN of) (NP (NP (DT an) (NN oath)) (PRN (-LRB- -LRB-) (NP (NN Section) (CD 156)) (-RRB- -RRB-))))))))))) (. .)))"""

def toNLTKtree(str):
    newTree = ParentedTree.fromstring(str)
    return newTree
        
def removeWP(tree = parsedSent):
    tree = str(tree)
    tree = " ".join(" ".join(tree.split("\n")).split())
    return tree

def ifThereIsNo(tree, toNotMatch):
    if toNotMatch == '':
        return True
    for node in tree:
        if type(node) is ParentedTree:
            #~ print "toNotMatch", toNotMatch, str(node.label())
            if re.match(toNotMatch, str(node.label())):
                #~ print "If there is no", toNotMatch, str(node.label())
                return False
    return True

def ifThereIsNoMatch(tree, toNotMatch):
    if toNotMatch == '':
        return True
    #print removeWP(tree)
    if re.match(toNotMatch, removeWP(tree)):
        return False
    return True

def tagChanger(TreeString, SubTreeString, toChange, newValue):
    TreeString = removeWP(str(TreeString))
    SubTreeString = removeWP(str(SubTreeString))
    toChange = re.sub("\^|\$",'', toChange) #Warning!!! Manual sub
    fixedSubTreeString = re.sub(toChange, newValue, SubTreeString, 1)
    #print fixedSubTreeString, toChange, newValue
    newTree = re.sub(re.escape(SubTreeString), fixedSubTreeString, TreeString, 1)
    #print "\n",newTree,"\n"
    return toNLTKtree(newTree)

def tagReplace(TreeString, SubTreeString, toChange, newValue):
    TreeString = removeWP(str(TreeString))
    SubTreeString = removeWP(str(SubTreeString))
    toChange = re.sub("\^|\$",'', toChange) #Warning!!! Manual sub
    fixedSubTreeString = re.sub(toChange, newValue, SubTreeString)
    #~ print fixedSubTreeString, toChange, newValue
    newTree = re.sub(re.escape(SubTreeString), fixedSubTreeString, TreeString)
    #~ print "\n",newTree,"\n"
    return toNLTKtree(newTree)

def findPredicate(parent, predicate, toMatch, toIgnore, found=None):
    if found:
        return found
    for node in parent:
        if type(node) is ParentedTree:
            if node.label() == predicate:
                continue
            if re.match(toMatch, node.label()) != None:
                #~ print toMatch, "matches '", node.label(),"'"
                if ifThereIsNo(node, toIgnore):
                    found = node
                    #print node.label()
                    return found
            found = findPredicate(node, predicate, toMatch, toIgnore, found)
    return found

#~ def findBinary(parent, predicate, toIgnore, found=None):
    #~ if found:
        #~ return found
    #~ for node in parent:
        #~ if type(node) is ParentedTree:
            #~ if node.label() == predicate:
                #~ continue
        #~ if ifThereIsNo(node, toIgnore):
            #~ found = node
            #~ return found
            #~ found = findPredicate(node, predicate, toMatch, toIgnore, found)
    #~ return found

def replacePredicate(inputTree, predicate, toMatch, toIgnore):
    while findPredicate(inputTree, predicate, toMatch, toIgnore):
        unaryStr = removeWP(str(findPredicate(inputTree, predicate, toMatch, toIgnore)))
        inputTree = tagChanger(inputTree, unaryStr, toMatch, predicate)
    return inputTree

def replaceKeywordPredicates(inputTree):
    inputTree = tagReplace(inputTree, "(IN If)", "^IN$", "Func")
    inputTree = tagReplace(inputTree, "(IN if)", "^IN$", "Func")
    inputTree = tagReplace(inputTree, "(IN then)", "^IN$", "Func")
    inputTree = tagReplace(inputTree, "(IN or)", "^IN$", "Func")
    inputTree = tagReplace(inputTree, "(IN and)", "^IN$", "Func")
    inputTree = tagReplace(inputTree, "(RB then)", "^RB$", "Func")
    inputTree = tagReplace(inputTree, "(RB not)", "^RB$", "Func")
    inputTree = tagReplace(inputTree, "(CC or)", "^CC$", "Func")
    return inputTree

#~ def replaceBinaryPredicates(inputTree, predicate, toMatch, toIgnore):
    #~ while findPredicate(inputTree, predicate, toMatch, toIgnore):
        #~ unaryStr = removeWP(str(findPredicate(inputTree, predicate, toMatch, toIgnore)))
        #~ inputTree = tagChanger(inputTree, unaryStr, toMatch, predicate)
    #~ return inputTree

#def outputUnaries(inputTree):
#    print findPredicate(inputTree, 'Unary', 'Unary', '')
    
def stringParser(parsedSent):
    inputTree = toNLTKtree(parsedSent)
    inputTree = replaceKeywordPredicates(inputTree)
    #Rule for functions
    #~ inputTree = replacePredicate(inputTree, 'Func', 'CC', '')
    #Rule for Unary
    inputTree = replacePredicate(inputTree, 'Unary', 'WHNP', '(.*)(VP|Func|VBG)(.*)')
    inputTree = replacePredicate(inputTree, 'Unary', '^NP$', '(.*)(VP|Func|VBG)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'VP', '(.*)\((Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'VP', '^((?!V[A-Z].?).)*$')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'VB[A-Z]?', '(.*)(Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'JJ', '(.*)(Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'TO', '(.*)(Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'MD', '(.*)(Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'IN', '(.*)(Unary|Func|Binary)(.*)')
    return inputTree
    

if __name__ == "__main__":
    parsed = stringParser(parsedSent)
    #~ print "Writing out put to parsedTree.txt"
    open("parsedTree.txt","w").write(str(parsed))

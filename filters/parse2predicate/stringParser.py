import re
from nltk import ParentedTree

parsedSent = """(ROOT
  (SBARQ
    (WHNP (WP Whoever))
    (SQ
      (VP
        (PP (CC upon)
          (NP
            (NP (NN commission))
            (PP (IN of)
              (NP (DT the) (NN act)))))
        (VBZ is)
        (ADJP (JJ incapable)
          (PP (IN of)
            (S
              (VP
                (VP (VBG appreciating)
                  (NP
                    (NP (DT the) (NNS wrongfulness))
                    (PP (IN of)
                      (NP (DT the) (NN act)))))
                (CC or)
                (VP (VBG acting)
                  (PP (IN in)
                    (NP
                      (NP (NN accordance))
                      (PP (IN with)
                        (NP (JJ such) (NN appreciation)))))
                  (NP
                    (ADJP (JJ due)
                      (PP (TO to)
                        (NP
                          (NP (DT a) (JJ pathological) (JJ emotional) (NN disorder))
                          (, ,)
                          (NP
                            (NP (JJ profound) (NN consciousness) (NN disorder))
                            (, ,)
                            (NP (JJ mental) (NN defect))
                            (CC or)
                            (NP (DT any) (JJ other) (JJ serious) (JJ emotional) (NN abnormality)))
                          (, ,))))
                    (NNS acts))
                  (PP (IN without)
                    (NP (NN guilt))))))))))))
"""

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
            print "toNotMatch", toNotMatch, str(node.label())
            if re.match(toNotMatch, str(node.label())):
                print "If there is no", toNotMatch, str(node.label())
                return False
    return True

def ifThereIsNoMatch(tree, toNotMatch):
    if toNotMatch == '':
        return True
    print removeWP(tree)
    if re.match(toNotMatch, removeWP(tree)):
        return False
    return True

def tagChanger(TreeString, SubTreeString, toChange, newValue):
    TreeString = removeWP(str(TreeString))
    SubTreeString = removeWP(str(SubTreeString))
    toChange = re.sub("\^|\$",'', toChange) #Warning!!! Manual sub
    fixedSubTreeString = re.sub(toChange, newValue, SubTreeString, 1)
    #~ print fixedSubTreeString, newValue
    newTree = re.sub(re.escape(SubTreeString), fixedSubTreeString, TreeString, 1)
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
    inputTree = tagChanger(inputTree, "(IN If)", "^IN$", "Func")
    inputTree = tagChanger(inputTree, "(IN if)", "IN", "Func")
    inputTree = tagChanger(inputTree, "(IN then)", "IN", "Func")
    inputTree = tagChanger(inputTree, "(IN or)", "^IN$", "Func")
    inputTree = tagChanger(inputTree, "(IN and)", "IN", "Func")
    inputTree = tagChanger(inputTree, "(RB then)", "RB", "Func")
    inputTree = tagChanger(inputTree, "(RB not)", "RB", "Func")
    
    return inputTree

#~ def replaceBinaryPredicates(inputTree, predicate, toMatch, toIgnore):
    #~ while findPredicate(inputTree, predicate, toMatch, toIgnore):
        #~ unaryStr = removeWP(str(findPredicate(inputTree, predicate, toMatch, toIgnore)))
        #~ inputTree = tagChanger(inputTree, unaryStr, toMatch, predicate)
    #~ return inputTree

#def outputUnaries(inputTree):
#    print findPredicate(inputTree, 'Unary', 'Unary', '')
    
if __name__ == "__main__":
    inputTree = toNLTKtree(parsedSent)
    inputTree = replaceKeywordPredicates(inputTree)
    #Rule for functions
    #~ inputTree = replacePredicate(inputTree, 'Func', 'CC', '')
    #Rule for Unary
    inputTree = replacePredicate(inputTree, 'Unary', 'WHNP', '(.*)VP(.*)')
    inputTree = replacePredicate(inputTree, 'Unary', '^NP$', '(.*)VP(.*)')

    #~ inputTree = replacePredicate(inputTree, 'Binary', 'VP', '(.*)\((Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'VP', '^((?!V[A-Z].?).)*$')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'VB[A-Z]?', '(.*)(Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'JJ', '(.*)(Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'TO', '(.*)(Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'MD', '(.*)(Unary|Func|Binary)(.*)')
    #~ inputTree = replacePredicate(inputTree, 'Binary', 'IN', '(.*)(Unary|Func|Binary)(.*)')
    
    #~ print inputTree
    open("parsedTree.txt","w").write(str(inputTree))
    #outputUnaries(inputTree)

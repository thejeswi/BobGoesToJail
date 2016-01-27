import re
from nltk import ParentedTree

parsedSent = """(ROOT
  (SBAR (IN If)
    (S
      (S
        (NP (DT the) (NN perpetrator))
        (VP (VBZ exceeds)
          (S
            (NP
              (NP (DT the) (NNS limits))
              (PP (IN of)
                (NP (JJ necessary) (NN defense))))
            (ADJP (JJ due)
              (PP (TO to)
                (NP (NN confusion) (, ,) (NN fear)
                  (CC or)
                  (NN fright)))))))
      (, ,) (RB then)
      (S
        (NP (PRP he))
        (VP (MD shall) (RB not)
          (VP (VB be)
            (VP (VBN punished))))))))
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
            if re.match(toNotMatch, str(node.label())):
                return False
    return True

def tagChanger(TreeString, SubTreeString, toChange, newValue):
    TreeString = removeWP(str(TreeString))
    SubTreeString = removeWP(str(SubTreeString))
    fixedSubTreeString = re.sub(toChange, newValue, SubTreeString, 1)
    #~ print fixedSubTreeString
    newTree = re.sub(re.escape(SubTreeString), fixedSubTreeString, TreeString, 1)
    #print newTree
    return toNLTKtree(newTree)

def findPredicate(parent, predicate, toMatch, toIgnore, found=None):
    if found:
        return found
    for node in parent:
        if type(node) is ParentedTree:
            if node.label() == predicate:
                continue
#            if node.label() == toMatch:
            if re.search(toMatch, node.label()):
                print toMatch, "matches", node.label()
                if ifThereIsNo(node, toIgnore):
                    found = node
                    #print node.label()
                    return found
            found = findPredicate(node, predicate, toMatch, toIgnore, found)
    return found

def replacePredicate(inputTree, predicate, toMatch, toIgnore):
    while findPredicate(inputTree, predicate, toMatch, toIgnore):
        unaryStr = removeWP(str(findPredicate(inputTree, predicate, toMatch, toIgnore)))
        inputTree = tagChanger(inputTree, unaryStr, toMatch, predicate)
    return inputTree

def replaceKeywordPredicates(inputTree):
    inputTree = tagChanger(inputTree, "(IN If)", "^IN$", "Func")
    inputTree = tagChanger(inputTree, "(IN if)", "IN", "Func")
    inputTree = tagChanger(inputTree, "(IN then)", "IN", "Func")
    inputTree = tagChanger(inputTree, "(IN or)", "IN", "Func")
    inputTree = tagChanger(inputTree, "(IN and)", "IN", "Func")
    inputTree = tagChanger(inputTree, "(RB then)", "RB", "Func")
	
    return inputTree

def replaceBinaryPredicates(inputTree, predicate, toMatch, toIgnore):
    while findPredicate(inputTree, predicate, toMatch, toIgnore):
        unaryStr = removeWP(str(findPredicate(inputTree, predicate, toMatch, toIgnore)))
        inputTree = tagChanger(inputTree, unaryStr, toMatch, predicate)
    return inputTree

#def outputUnaries(inputTree):
#    print findPredicate(inputTree, 'Unary', 'Unary', '')
    
if __name__ == "__main__":
    inputTree = toNLTKtree(parsedSent)
    inputTree = replaceKeywordPredicates(inputTree)
    #Rule for functions
    inputTree = replacePredicate(inputTree, 'Func', 'CC', '')
    #Rule for Unary
    inputTree = replacePredicate(inputTree, 'Unary', 'NP', 'VP|Unary')
    

    inputTree = replacePredicate(inputTree, 'Binary', '^((?!S).)*$', 'SBAR')
    print inputTree
#    outputUnaries(inputTree)

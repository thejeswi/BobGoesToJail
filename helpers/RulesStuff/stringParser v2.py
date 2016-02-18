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
    return toNLTKtree(re.sub(re.escape(SubTreeString), fixedSubTreeString, TreeString, 1))

def findPredicate(parent, predicate, toMatch, toIgnore, found=None):
    if found:
        return found
    for node in parent:
-        if type(node) is ParentedTree:
            if node.label() == predicate:
                continue
            if node.label() == toMatch:
                if ifThereIsNo(node, toIgnore):
                    found = node
            print found
            found = findPredicate(node, predicate, toMatch, toIgnore, found)
    return found

def replacePredicate(inputTree = toNLTKtree(parsedSent), predicate='Unary', toMatch='NP', toIgnore='VP|Unary'):
    while findPredicate(inputTree, None, predicate, toMatch, toIgnore):
        unaryStr = removeWP(str(findPredicate(inputTree, predicate, toMatch, toIgnore)))
        inputTree = tagChanger(inputTree, unaryStr, toMatch, predicate)
    return inputTree
    
if __name__ == "__main__":
    inputTree = toNLTKtree(parsedSent)
    #Rule for functions
    inputTree = replacePredicate(inputTree, predicate='Func', toMatch='CC', toIgnore='ZZ')
    inputTree = replacePredicate(inputTree, predicate='Unary', toMatch='NP', toIgnore='VP|Unary')
    print inputTree

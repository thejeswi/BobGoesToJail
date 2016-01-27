import re
from nltk import ParentedTree

import os
clear = lambda: os.system('clear')

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
            (VP (VBN punished))))))))"""

def toNLTKtree(str):
    newTree = ParentedTree.fromstring(str)
    return newTree
        
def removeWP(tree = parsedSent):
    tree = str(tree)
    tree = " ".join(" ".join(tree.split("\n")).split())
    return tree

def ifThereIsNo(tree, toNotMatch):
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

def findUnary(parent, found=None):
    if found:
        return found
    for node in parent:
        if type(node) is ParentedTree:
            if node.label() == 'Unary':
                continue
            if node.label() == 'NP':
                if ifThereIsNo(node, "VP|Unary"):
                    found = node
            found = findUnary(node, found)
    return found

def toUnary(inputTree = toNLTKtree(parsedSent)):
    while findUnary(inputTree):
        unaryStr = removeWP(str(findUnary(inputTree)))
        inputTree = tagChanger(inputTree, unaryStr, "NP", "Unary")
    return inputTree
    
print toUnary()

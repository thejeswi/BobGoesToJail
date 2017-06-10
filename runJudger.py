from filters.text2parse import client
from filters.parse2predicate import stringParser, treeToString

import sys
sys.path.append('/home/mlc/BobGoesToJail/judge')

from judge.judger import run as judge

def getParseTrees(case):
    parsed = nlp.parse(case)
    for sent in parsed["sentences"]:
        yield sent["parsetree"]

def getListFromTrees(parseTrees):
    for pTree in parseTrees:
        listOfTuples = treeToString.treeToString(str(pTree))
        yield listOfTuples
        
def getRuledTrees(parseTrees):
    for pTree in parseTrees:
        treeWithRules = stringParser.stringParser(pTree)
        yield treeWithRules

def process_case(case):
    global nlp
    nlp = client.StanfordNLP()
    #Run Stanford NLP
    parseTrees = getParseTrees(case)
    #Run all the tree rules
    ruledTrees = getRuledTrees(parseTrees)
    #Convert the tree to lists of tuples
    cWords = []
    for t in getListFromTrees(ruledTrees):
        cWords.append(t)
        print t
    return cWords

def get_bob(caseWordsList):
    bob = []
    nonBob = []
    for caseWords in caseWordsList:
        for i in range(len(caseWords)):
            if caseWords[i][1][0].lower() == "bob" or caseWords[i][1][0].lower() == "john":
                bob.append(caseWords[i][1][0].strip())
            else:
                nonBob.append(caseWords[i][1])
    bob = list(set(bob))
    return (bob, nonBob)
        
def run(inputCase):
    print inputCase
    caseWords = process_case(inputCase)
    bobs, nonBobs = get_bob(caseWords)
    actions = []
    for n in nonBobs:
        actions.append(" ".join(n).strip())
    print "Action: ", actions
    case = { "Persons" : bobs, 
        "Action": {	"Bob" : actions}, 
        "Act" : inputCase
        }
    print case
    return judge(case)
    #~ case = { "Persons" : ["Bob"], 
		#~ "Action": {	"Bob" : ["induces", "killed a human", "carelessness"]}, 
		#~ "Act" : "Bob causes death of a human through shortcoming"}


if __name__ == "__main__":
    print "Welcome to BobGoesToJail?"
    print "Example input: Bob causes death of a human through carelessness\nPlease input a case:"
    #inputCase = raw_input()
    
    inputCase = "Bob walks on the Great wall of china" 
    #~ inputCase = "A human was killed of negligence by Bob" 
    #~ inputCase = "Bob negligently induces physical harms to another human" # works
    #inputCase = "Bob killed a human by carelessness"  # works
    #inputCase = "Bob knowingly interrupts a burial" # works
    #inputCase = "Bob unknowingly interrupts a burial" # if it works, it should find nothing
    #inputCase = "Bob disparages memory of a dead person" # works
    
    output = run(inputCase)
    #~ print "Output: ", output
    
    
    

import pdb
from rules import rules

ruleTexts = [rule[0].lower().strip() for rule in rules]

def ruleReplace(combinedList):
    finalList = []
    for _tuple in combinedList:
        phrase = " ".join(_tuple[1]).lower().strip()
        #Warning! This is dangerous!
        #Replacing original text with new text, if a similar match is found
        if phrase in ruleTexts:
            ruleFound = ruleTexts.index(phrase)
            finalList.append((rules[ruleFound][1],_tuple[1]))
            print "New text: ", list(rules[ruleFound][0].split(" "))
            print "New text: ", _tuple[1]
        else:
            finalList.append(_tuple)
    return finalList

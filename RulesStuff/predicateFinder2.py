parsedSent = """(ROOT
  (S
    (NP
      (NP (DT A) (NN child))
      (PP (IN under)
        (ADJP
          (NP (CD 10) (NNS years))
          (JJ old))))
    (VP (VBZ is) (RB not)
      (ADJP (RB criminally) (JJ responsible)
        (PP (IN for)
          (NP (DT an) (NN offence)))))
    (. .)))"""




import re

unaryRule = ["\(NP (.*)\)\n", "\(ADJP (.*)\)\n"]
unaryMatches = re.findall( unaryRule, parsedSent)
print unaryMatches

binaryRules = ["\(VBZ (.*)\)\n", "\(IN (.*)\)\n"]
binaryMatches = re.findall(binaryRule, parsedSent)
print binaryMatches




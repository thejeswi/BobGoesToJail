parsedSent = """(ROOT
  (S
    (NP
      (NP (DT A)
	(NN child))
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
#\(NP !(\([\w ]*\)\s?)+!

unaryRule1 = re.compile("\(NP (.*)")
for m in unaryRule1.finditer(parsedSent):
	pos = m.start()
	
	ctr = 0
	beginBracket = re.compile("\(")
	for b in beginBracket.finditer(parsedSent[pos:]):
		bracketPos = b.start()
		ctr = ctr + 1		

		endBracket = parsedSent[bracketPos:].find("\)")

		for e in endBracket.finditer(parsedSent[bracketPos:]):
			bracketEndPos
	

#matches = re.findall (unaryRule1, parsedSent)
#print matches


unaryRules = ["\(NP (.*)\)", "\(ADJP [A-Za-z0-9]*\)"]
for unaryRule in unaryRules:
	unaryMatches = re.findall( unaryRule, parsedSent)
	print "Unary:",unaryMatches

binaryRules = ["\(VBZ [A-Za-z0-9]*\)", "\(IN [A-Za-z0-9]*\)"]
for binaryRule in binaryRules:
	binaryMatches = re.findall(binaryRule, parsedSent)
	print "Binary:",binaryMatches




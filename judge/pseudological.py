import nltk, nltk.data, nltk.tag
#tagger = nltk.data.load(nltk.tag._POS_TAGGER)

def replaceFuncToHtml(text):
	text = text.replace('or', '&or;')
	text = text.replace('and', '&and;')
	text = text.replace('not', '&not;')
	#text = text.replace('shall', '&rArr;')
	text = text.replace('(IMPL)', '&rArr;')
	text = text.replace('(CIMPL)', '&lArr;')
	return text
		
def getSentencesArraySplitByDot(db_ent, sent_obj_id):
	sents = []
	

	db_entries = db_ent.find({'sentenceID':sent_obj_id})
	
	curSent = []
	curSent.append(['[', 'Func']) # add sent begin bracket
	for _entity in db_entries:
		if not _entity['text']:
			continue
			
		text = ' '.join(_entity['text'])
			
		#print text
		entityType = _entity['entityType']
		
		if len(curSent) == 0:
			curSent.append(['[', 'Func']) # add sent begin bracket
		
		curSent.append([text, entityType])
		
		if text == '.':
			curSent.append([']', 'Func']) # add sent end bracket
			sents.append(curSent)
			curSent = []
		
	if len(curSent) > 0:
		sents.append(curSent)
	
	return sents	
	

def ifToLogical(sents):
	sentsOut = []
	ifInBeginning = False

	for sent in sents:
		entities = []
		for _entity in sent:
			text = _entity[0]
			entityType = _entity[1]
			
			if '.' in text: # Finished sentence
				# reset flags
				ifInBeginning = False

			
			if entityType == 'Func':
				if text == 'If': #if in the beginning of the sent
					ifInBeginning = True
					continue # remove if in the beginning
				elif 'if' in text: #if within the entity
					_entity[0] = '(CIMPL)'
				elif 'then' in text and not ('if' in sent or 'If' in sent):
					_entity[0] = '(IMPL)'
				if ifInBeginning:
					if text == 'then':
						_entity[0] = '(IMPL)'
				# TODO: if not: search for first komma followed by unary predicate and place then there
		
			entities.append(_entity)
		sentsOut.append(entities)
	return sentsOut
	
	
def implDotFinder(entities):
	implPositions = []
	dotPositions = []

	for i, _entity in enumerate(entities):
		text = _entity[0]
		entityType = _entity[1]
		
		# search for (IMPL) and (CIMPL)
		if '(IMPL)' in text or '(CIMPL)' in text:
			implPositions.append(i)
		elif '.' in text:
			dotPositions.append(i)
		
	return (implPositions, dotPositions)

def textFuncFinder(entities, text, type):
	#return positions
	return [i for i, _entity in enumerate(entities) if _entity[0].lower() == text.lower() and _entity[1] == type]
	
def splitByDotsArray(dotPositions):
	for dotPos in dotPositions:
		if i < dotPos: # Within a sent
			for implPos in implPositions:
				return implPos < dotPos
	return False
	
def setBracketsImpl(sent):
	positions = implDotFinder(sent)
	implPositions = positions[0]
	dotPositions = positions[1]
	
	#Check if there is a implication within the current sent
	if len(implPositions) == 0 or len(dotPositions) == 0: 
		# no implications found, we dont have to fix anything
		return sent

	i = 0
	entitiesOut = []
	for _entity in sent: 
		text = _entity[0]
		entityType = _entity[1]
		
		# start		
		if i == 0:
			entitiesOut.append(['[','Func'])
			
		# front
		if i in implPositions:
			entitiesOut.append([']','Func'])
			
		# back
		if (i-1) in implPositions:
			entitiesOut.append(['[','Func'])
		
		entitiesOut.append(_entity)
		
		#end
		if i in dotPositions:
			entitiesOut.append([']','Func'])
			
		i = i + 1
		
	return entitiesOut
	
def setBracketsOrAnd(sent):
	outputSent = []
	lBracket = ('[f', 'Func')
	rBracket = ('f]', 'Func')
	
	setRightBracket = False
	
	a = 0
	for i, _entity in enumerate(sent): 
		text = _entity[0]
		entityType = _entity[1]
		
		#a = len(outputSent)
		
		if entityType == "Func" and (text == "or" or text == "and"):
			
			if a-1 in range(len(sent)) and a+1 in range(len(sent)):
				leftEnt = sent[a-1]
				rightEnt = sent[a+1]
				
				# Rule 1: Set brackets [Unary and Unary]
				unUnRule = leftEnt[1] == "Unary" and rightEnt[1] == "Unary"
				
				# Rule 2: Set brackets [Binary or Binary]
				biBiRule = leftEnt[1] == "Binary" and rightEnt[1] == "Binary"
				
				# Rule 3: Set brackets [ADV or ADV]
				advRule = leftEnt[1] == "ADV" and rightEnt[1] == "ADV"
				
				# Rule 3: Set brackets [Unary and Binary Unary Binary Unary ...][
				# TODO
				
				if unUnRule or biBiRule or advRule:
					outputSent.insert(a-1, lBracket)
					outputSent.append(_entity)
					a += 1
					setRightBracket = True
					continue

		outputSent.append(_entity)
		a += 1
			
		if setRightBracket:
			setRightBracket = False
			outputSent.append(rBracket)
			#a += 1
	
	return outputSent
	
def setOrAndWithinUnary(sent):
	outputSent = []
	lBracket = ('[u', 'Func')
	rBracket = ('u]', 'Func')
	funcOr = ('or', 'Func')
	funcAnd = ('and', 'Func')
	
	for i, _entity in enumerate(sent): 
		text = _entity[0]
		entityType = _entity[1]
	
		# Rule: Find or/and within Unary: Unary => [Unary or/and Unary]
		andRule = ' and ' in text
		orRule = ' or ' in text
		if andRule or orRule:
			outputSent.append(lBracket)
			
			if andRule:
				splitBy = ' and '
				replaceFunc = funcAnd
			elif orRule:
				splitBy = ' or '
				replaceFunc = funcOr			
			
			unaryParts = text.split(splitBy)

			# Rule: Replace the , with the found function: , => or
			for unaryPart in unaryParts:
				if ',' in unaryPart:
					commaParts = unaryPart.split(',')
					for commaPart in commaParts:
						if commaPart != '':
							outputSent.append((commaPart.replace('^\b+', '').replace('\b+$', ''), 'Unary'))
							outputSent.append(replaceFunc)
				else:
					outputSent.append((unaryPart, 'Unary'))
					outputSent.append(replaceFunc)
			outputSent.pop() # pop last or
			
			outputSent.append(rBracket)
		else:
			outputSent.append(_entity)
	
	return outputSent
	
def splitAdverbesInBinary(sent):
	outputSent = []
	lBracket = ('[a', 'Func')
	rBracket = ('a]', 'Func')
	funcOr = ('or', 'Func')
	funcAnd = ('and', 'Func')
	
	for i, _entity in enumerate(sent): 
		text = _entity[0]
		entityType = _entity[1]
		
		if entityType == 'Binary':
			#run nltk pos-tagger on text
			print "postagging"
			tags = nltk.pos_tag(nltk.word_tokenize(text))
			print tags
			print "postagging done"
			# Rule: Split adverbs within Binary: Binary => [Binary and Adjective and Binary]
			newEntities = []
			restBinary = ""
			
			isAdjInBinary = len([word for word, tag in tags if tag == 'JJ']) > 0
			
			if isAdjInBinary:
				newEntities.append(lBracket)
			
				for wordtxt, tag in tags:
					if tag == 'RB':
						if restBinary != "":
							newEntities.append((restBinary, 'Binary'))
							newEntities.append(funcAnd)
							restBinary = ""
							
						newEntities.append((wordtxt, 'Binary'))
						newEntities.append(funcAnd)
					else:
						restBinary += wordtxt + ' '
									
				if restBinary != "":
					newEntities.append((restBinary[:-1], 'Binary'))
					
				newEntities.append(rBracket)
				outputSent.extend(newEntities)
			else:
				outputSent.append(_entity)		
		else:
			outputSent.append(_entity)
		
	return outputSent
	
def bracketSetter(sents):		
	return [setOrAndWithinUnary(setBracketsOrAnd(setBracketsImpl(sent))) for sent in sents]
	
def filterSymbols(sents):
	sentsOut = []

	for sent in sents:
		entities = []
		lastSym = ""
		for i in range(len(sent)):
			_entity = sent[i]

			text = _entity[0]
			entityType = _entity[1]

			#remove .
			if text == '.':
				continue
			
			if (i+1) < len(sent):
				next_entity = sent[i+1]
				next_text = next_entity[0]
				next_type = next_entity[1]
				
				#remove , from ,(Func)
				if text == ',' and next_type == 'Func':
					continue


			entities.append(_entity)
			
		sentsOut.append(entities)
	return sentsOut
		
def filterSents(db_ent, sent_obj_id):
	return filterSymbols(bracketSetter(ifToLogical(getSentencesArraySplitByDot(db_ent, sent_obj_id))))

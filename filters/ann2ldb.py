def searchIndexList(lawTxt, index):
    i = -1
    entityNr = -1

    for entity in lawTxt:
        if index <= i:
            return entityNr
        
        if(entity != '###'):
            i = i + len(entity)
        
        i = i + 1
        entityNr = entityNr + 1  
    return entityNr
        
def findAnnotations(lawTxt, start, end):
    startCell = searchIndexList(lawTxt, start)
    endCell = searchIndexList(lawTxt, end)

    #print "Starts in cell", startCell, "and ends in cell", endCell 

    tags = []
    for i in range(startCell, endCell+1):
        tags.append(posTags[i])

    return tags
        
def annPOSTagger(txtFile,annFile):    
    fAnn = open(annFile)
    fTxt = open(txtFile)
    annTxt = fAnn.read()
    lawTxt = fTxt.read()
    
    lawTxtWordList = lawTxt.replace("\n", " ").split(" ")
    
    filteredLawTxtList = []
    for word in lawTxtWordList:
        if word == '':
            filteredLawTxtList.append("###")
        else:
            filteredLawTxtList.append(word.strip(";"))
            
    posTags = nltk.pos_tag(filteredLawTxtList)
    engine = create_engine('sqlite:///../DB/entity.db')
    Base.metadata.bind = engine 
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for entity in annTxt.split("\n"):
        if len(entity) > 0 and entity[0] == "T":
            obj = entity.split("\t")
            
            annTag = obj[0]
            
            word = obj[1].split(" ")
            start = int(word[1])
            end = int(word[2])
    
            entity = word[0]
            phrase = obj[2]
            newLocation = Location(annFile, start, end, annTag)
            session.add(newLocation)
            session.commit()
            for word in pharse.split(" "):
                newEntity = Entity(word, entity, )


#print annotations

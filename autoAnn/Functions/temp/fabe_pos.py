import nltk
fAnn = open("14.ann")
annTxt = fAnn.read()

entityList = []

for entity in annTxt.split("\n"):
    if len(entity) > 0 and entity[0] == "T":
        obj = entity.split("\t")
        
        word = obj[1].split(" ")
        start = word[1]
        end = word[2]

        entity = word[0]
        phrase = obj[2]
        
        entityList.append([start, end, entity, phrase])
        
for entity in entityList:
	print entity

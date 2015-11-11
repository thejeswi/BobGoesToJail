fileTxt = open("14.ann").read()
senList = fileTxt.split("\n")
delimit = "$#$"
POS_list = []
for sen in senList:
	if len(sen) > 0 and sen[0] == "T":
		obj = sen.split("\t")
		idTag = obj[0]
		words = obj[2].split(" ")
		words.append(delimit+idTag)
		POS_list.extend(words)
import nltk
taggedList = nltk.pos_tag(POS_list)
outFileTxt = ""
for element in taggedList:
	if element[0][0:2] == "$#$":
		outFileTxt = outFileTxt + "\n"
	else:
		outFileTxt = outFileTxt + element[0]+"\\"+element[1]+" "
outFile = open("14.annpos","w")
outFile.write(outFileTxt)

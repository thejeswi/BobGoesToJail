from finder_client import get_relavent_laws, get_similarity

def similarityCheck(actText, entText):
	# TODO: Implement word2vec similarity check with threshold similarity value?
	similarity = 0
	count = 0
	for actWord in actText.split(" "):
		for entWord in entText.split(" "):
			sim = float(get_similarity(actWord, entWord))
			if sim < 0.5:
				continue
			print entWord, actWord, sim
			similarity += sim
			count += 1
	threshold = 0.8 
	print similarity
	score = similarity / count
	out = score >= threshold 
	print score
	return out

print similarityCheck("funeral service","funeral service")

from nltk.tree import Tree

def traverse(t, wordList = []):
    try:
        t.label()
    except AttributeError:
        return wordList.append(t)
    else:
        for child in t:
            traverse(child, wordList)
    return wordList

if __name__ == "__main__":    
    t = Tree.fromstring('(S (NP Alice) (VP chased (NP the rabbit)))')
    print traverse(t)
    

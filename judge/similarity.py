from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":
   sent1 = "possession of stolen property"
   sent2 = "mongo"
   print similar(sent1,sent2)

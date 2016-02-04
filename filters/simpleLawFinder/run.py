from pymongo import MongoClient

lawDB = "law_db"

dbClient = MongoClient()
lawsDB = dbClient[lawDB]
laws_db = lawsDB.laws

def noSubLaw():
    "Return all laws with no subLaws"
    found_laws = laws_db.find({"title":{"$exists": True}})
    law_id = None
    simpleLaws = []
    for law in found_laws:
        filtered_law_texts = []
        if "title" in law:
            law_id = law["_id"]
            filtered_laws = laws_db.find({"lawID":law_id})
            count = 0
            for _law in filtered_laws:
                if "text" in _law:
                    filtered_law_texts.append(_law)
                    count += 1
            if count == 1:
                simpleLaws.extend(filtered_law_texts)

    return simpleLaws


def simpleLaws2File():
    found_laws = noSubLaw()
    count = 0
    print "Working on law number:"
    for law in found_laws:
        sentenceID = law["_id"]
        lawText = law["text"]
        f = open("./simpleLaws/"+str(sentenceID)+".txt","w")
        f.write(str(lawText))
        f.close()

if __name__ == "__main__":
    simpleLaws2File()

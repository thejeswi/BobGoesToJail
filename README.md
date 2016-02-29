# Bob goes to jail?
##A semantic Law Interpreter

Welcome! Thank you for using BobGoesToJail?
We hope you don't go to jail.

To run the judging program, use python runJudger.py

#Requirements:
* Mongo server running on 'localhost', port: 27017
* coreNLP server running on 'localhost', port: 3456
* Word2Vec server running 'localhost', port: 9090
* Python libraries required are listed on requirements.txt
    Use "pip install -r requirements.txt" to install them.

#Major Modules:
##Filters
###Things which convert one data format to another.
It includes different filter which convert german law text files to a pseudo semantic form, one step a time.
Each of the below mentioned modules have a run.py file.
Modules which do it are:
* corpus2db: Inserts content pf splitted law text file to database. Also stores the Law number of the law and other attributes.
    This function module is now decaprecated. Use lawSplitter.py in the project root folder.
* text2parse: Use law texts to get parse trees of each sentence.
    To use run: python run.py
* parse2predicate: Extracts predicates from parse trees of laws in the database. To insert to database, use: python run.py insert
* simpleLawFinder: Finds simple laws which has no sublaws and store them to text files.
    To use run: python run.py

##Database
###Schema related things
Has schema files which are used by different modules. It is used to enforce uniformity in the database.

##Corpus
###The raw law texts
Nothing to run here.
Contains all the text files extracted for the source law text file.

#Judge
###The judging process
Contains all the scripts which are used for running the judging framework.
Nothing to directly run here. Use runJudger in the project root to use the judger.

# Bob goes to jail?
## A semantic Law Interpreter

Welcome! Thank you for using BobGoesToJail?
We hope you don't go to jail.



# Installation Requirements:
0. Clone BobGoesToJail using `git clone git@code.fg-tech.de:thejeswi/BobGoesToJail.git`
1. Mongo server running on 'localhost', port: 27017
    * On Debian based OS use `apt-get install mongodb`. For other operating systems, please refer https://www.mongodb.org/downloads
2. coreNLP server running on 'localhost', port: 3456
    * Use these commands:
        * `pip install pexpect unidecode`
        * `git clone git://github.com/dasmith/stanford-corenlp-python.git`
        * `cd stanford-corenlp-python`
        * `wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-08-27.zip`
        * `unzip stanford-corenlp-full-2014-08-27.zip`
    * Run: `python corenlp.py`
3. Word2Vec server running 'localhost', port: 9090

    * Go to `BobGoesToJail/word2vec`
    * Download `GoogleNews-vectors-negative300.bin.gz` from https://docs.google.com/uc?id=0B7XkCwpI5KDYNlNUTTlSS21pQmM&export=download in this folder
    * Run: `python run.py`
4. Python libraries required are listed on requirements.txt
    * Use `pip install -r requirements.txt` to install them.

5. Other package requirements: python-dev, curl

# Run instructions:
* To run the judging program, use python `run.py`
* For obtaining the Psuedo Logical form of the law for your own corpus, follow these steps:
    1. Get the law corpus as `txt` files into BobGoesToJail/corpus/lawTexts_en
    2. Run `python BobGoesToJail/lawSplitter.py`
    3. Run `python BobGoesToJail/filters/text2parse/run.py`
    4. Run `python BobGoesToJail/filters/parse2predicate/run.py insert`
    5. Run `python BobGoesToJail/filters/simpleLawFinder/run.py`

# Major Modules:
## Filters
### Things which convert one data format to another.
It includes different filter which convert german law text files to a pseudo semantic form, one step a time.
Modules which do it are:
* corpus2db: Inserts content pf splitted law text file to database. Also stores the Law number of the law and other attributes.
    This module is now decaprecated. **Use `python lawSplitter.py` in the project root folder.**
* text2parse: Use law texts to get parse trees of each sentence.
    To use run: `python run.py`
* parse2predicate: Extracts predicates from parse trees of laws in the database.
    To insert to database, use: `python run.py insert`
* simpleLawFinder: Finds simple laws which has no sublaws and store them to text files.
    To use run: `python run.py`

## Database
### Schema related things
Has schema files which are used by different modules. It is used to enforce uniformity in the database.

## Corpus
### The raw law texts
Nothing to run here.
Contains all the text files extracted for the source law text file.

# Judge
### The judging process
Contains all the scripts which are used for running the judging framework.
Nothing to directly run here. Use runJudger in the project root to use the judger.

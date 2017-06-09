from flask import Flask
from entity_matcher import similarity_finder
from law_matcher import law_matcher

import gensim

app = Flask(__name__)

print "Started loading"
model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin.gz', binary=True)
print "Done loading"
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/ent/<word1>/<word2>")
def ent(word1, word2):
    return str(similarity_finder(model, word1, word2))

@app.route("/law/<inputCase>")
def law(inputCase):
    print inputCase
    return str(law_matcher(model, inputCase))

if __name__ == "__main__":
    app.run(port=9090)

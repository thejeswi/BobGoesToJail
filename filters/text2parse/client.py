import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
#~ import jsonrpclib
from pprint import pprint
#from nltk.draw.util import CanvasFrame
#from nltk.draw import TreeWidget

class StanfordNLP:
    def __init__(self, port_number=8080):
        #~ self.server = jsonrpclib.Server("http://127.0.0.1:%d" % port_number)
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", port_number)))

    def parse(self, text):
        return json.loads(self.server.parse(text))

if __name__=="__main__":
    nlp = StanfordNLP()
    text = """A sentence here."""
    result = nlp.parse(text)
    f =open("outfile.txt","w")
    f.write(str(result))
    f.close()
    
    counter = 0
    #~ from nltk.tree import ParentedTree
    #~ for sent in result['sentences']:
        #~ sentence = sent['parsetree']
        #~ tree = ParentedTree.fromstring(sentence)
        #~ print tree
        #~ cf = CanvasFrame()
        #~ tc = TreeWidget(cf.canvas(),tree)
        #~ cf.add_widget(tc,10,10) # (10,10) offsets
        #~ cf.print_to_file('tree'+str(counter)+'.ps')
        #~ counter += 1
        #~ cf.destroy()

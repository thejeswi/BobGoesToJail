import json
# from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
from pprint import pprint
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

class StanfordNLP:
    def __init__(self, port_number=3456):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

if __name__=="__main__":
    nlp = StanfordNLP()
    text = """2 Temporal Applicability
        
        (1) The punishment and its collateral consequences are determined by the law which is in force at the time of the act.
        
        (2) If the threatened punishment is amended during the commission of the act, then the law shall be applicable which is in force at the time the act is completed.
        
        (3) If the law in force upon the completion of the act is amended before judgment, then the most lenient law shall be applicable.
        
        (4) A law, which was intended to be in force only for a determinate time, shall be applicable to acts committed while it was in force, even if it is no longer in force. This shall not apply to the extent a law provides otherwise.
        
        (5) Subsections (1) through (4) shall apply, correspondingly, to forfeiture, confiscation and rendering unusable.
        
        (6) Unless the law provides otherwise, decisions as to measures of reform and prevention shall be according to the law which is in force at the time of judgment."""
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

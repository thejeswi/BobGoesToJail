import datetime

class raw_law(object):
    """This is for unprocessed law text, straight from text file!"""
    def __init__(self):
        self.num = "Undefined",
        self.title = "Undefined",
        self.text = "Undefined",
        self.time = datetime.datetime.utcnow()
    def out(self):
        return {
                "num" : self.num,
                "title": self.title,
                "text": self.text,
                "time":self.time
                }

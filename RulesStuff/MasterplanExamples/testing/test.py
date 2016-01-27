import re
str = "None_1"
print re.match(r'/^None_[0-9]+$/', str) != None


var = ('Binary', 'hello world or whaat or test')

out = [('Binary','hello world'), ('Func', 'or'), ('Binary', 'what')]


final = []
spl = var[1].split(' or ')
for splE in spl:
	if splE == "or":
		final.append(('Func', splE))
	else:
		final.append(('Binary', splE))	

print final

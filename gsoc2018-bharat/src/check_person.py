import os
import re
import sys

def count_pronouns(
		filename, f):
	"""
	Takes the input file with the extracted text from the Wikipedia dump
	and finds whether given article is about a Male or a Female.

	Arguments
	---------
	filename : The input file.
	f : Output file with all the titles and
	their respective form ( Masculine / Feminine ).
	"""
	title = ''
	c = 0.02
	wc = 0
	masc_forms = ['he', 'him', 'his']
	mc = 0
	femi_forms = ['she', 'her', 'hers']
	fc = 0
	with open(f, 'w+') as output:
		with open(filename, 'r') as inp:
			for line in inp:
				if line.startswith("<doc"):
					title = next(inp).rstrip('\n').replace(' ', '_')
					continue
				else:
					wc += len(line.split())
					for form in masc_forms:
						mc += len(re.findall(r'\b'+ form + r'\b', line, re.IGNORECASE))
					for form in femi_forms:
						fc += len(re.findall(r'\b'+ form + r'\b', line, re.IGNORECASE))
				if line.startswith('</doc>'):
					if (mc/wc > c) or (fc/wc > c):
						if mc > fc:
							output.write(title + ',male')
							print(title + ',male')
						else:
							output.write(title + ',female')
							print(title + ',female')
					wc = mc = fc = nc = pc = 0

if __name__ == "__main__":
	directory, f = sys.argv[1], sys.argv[2]
	for root, dirs, files in os.walk(directory):
		for file in files:
			count_pronouns(root + '/' + file, f)
import os
import re
import sys

def p(a, b):
	return ',' + str(100*a/b)

def countPronouns(filename):
	people = []
	with open('dbo:Person', 'r') as op:
		for line in op:
			people.append(line.strip('\n'))
	title = ''
	wc = 0
	mascForms = ['he', 'him', 'his']
	mc = 0
	femiForms = ['she', 'her', 'hers']
	fc = 0
	# neutForms = ['it', 'its']
	# nc = 0
	# plurForms = ['they', 'them', 'their']
	# pc = 0
	with open('gender.csv', 'a+') as output:
		with open(filename, 'r') as inp:
			for line in inp:
				if line.startswith("<doc"):
					title = next(inp).rstrip('\n').replace(' ', '_')
					continue
				else:
					wc += len(line.split())
					for form in mascForms:
						mc += len(re.findall(r'\b'+ form + r'\b', line, re.IGNORECASE))
					for form in femiForms:
						fc += len(re.findall(r'\b'+ form + r'\b', line, re.IGNORECASE))
					# for form in neutForms:
					# 	nc += len(re.findall(r'\b'+ form + r'\b', line, re.IGNORECASE))
					# for form in plurForms:
					# 	pc += len(re.findall(r'\b'+ form + r'\b', line, re.IGNORECASE))
				if line.startswith('</doc>'):
					if (mc/wc > 0.02) or (fc/wc > 0.02):
						if mc > fc:
							output.write(title + ',male') #+ p(nc, wc) + p(pc, wc))
							print(title + ',male')
						else:
							output.write(title + ',female')
							print(title + ',female')
						# print(title + p(mc, wc) + p(fc, wc)) #+ p(nc, wc) + p(pc, wc))
					wc = mc = fc = nc = pc = 0

if __name__ == "__main__":
	directory = sys.argv[1]
	for root, dirs, files in os.walk(directory):
		for file in files:
			countPronouns(root + '/' + file)
import os, sys
import codecs
import json
import re

directory, file, output = sys.argv[1], sys.argv[2], sys.argv[3]

"""
Uncomment the following lines to count the unique resources in the entire corpus.
These are the injected entities which were tagged with the help of Surface Forms
generated from the original dump.
"""
# entities = set()
# for root, dirs, files in os.walk(directory):
# 	for f in files:
# 		path = root + '/' + f
# 		for line in codecs.open(path, 'r', encoding='utf-8', errors='ignore'):
# 			for ent in re.findall(r'(resource/)+(\w+)', line):
# 				entities.add(''.join(ent))
# 				print("Entities : " + str(len(entities)), end='\r')
# print("Entities : " + str(len(entities)))
# del entities

"""
Here I will create a dictionary containing the mappings
between the entities and their descriptions.
"""
def reader(fname):
	with codecs.open(path, 'r', encoding='utf-8', errors='ignore') as infile:
		prev = next(infile)
		for line in infile:
			yield prev, line
			prev = line

"""
The following snippet combines the different files extracted
using the extract.py script and creates a single file with
complete text that can be used to generate pre-trained embeddings.
"""
with open(file, 'w+') as outfile:
	for root, dirs, files in os.walk(directory):
		for f in files:
			print("Writing file " + str(root) + '/' + str(f))
			path = root + '/' + f
			with codecs.open(path, 'r', encoding='utf-8', errors='ignore') as infile:
				for line in infile:
					if '<doc' in line:
						pass
					else:

						# Obtain just the processed text from the multiple files
						outfile.write(line)

count = 0

# Pattern to extract title from the document url
pattern = r'(title=)+(.\w+.)*'
with open(output, 'w+') as outdict:
	for root, dirs, files in os.walk(directory):
		for f in files:
			path = root + '/' + f
			with codecs.open(path, 'r', encoding='utf-8', errors='ignore') as infile:
				for prev, line in reader(path):
					dictionary = {}
					if prev.startswith('<doc') and not line.startswith('<doc'):
						try:
							ent = re.search(pattern, prev).group().replace(' ', '_').replace('title="', '').strip('"')
							ent = "resource/" + ent
							
							# Line serves the purpose of description
							dictionary[ent] = line
							json.dump(dictionary, outdict)
							outdict.write('\n')
							count += 1
							print("Descriptions : " + str(count), end='\r')
							continue
						except:
							continue
					else:
						pass

print("Descriptions : " + str(count))
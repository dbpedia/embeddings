import re
import numpy as np
import sys

''' The tokenizePhrases replaces the anchor text by the linked entity name, if the linked entity name has spaces it replaces the spaces with undrerscores.with
	#wikilinks are marked by [[linked entity(|anchor text)]] is replaced with linked_entity as the output and saved to output_corpus.txt
	The linked entities along with their anchor words are stored in AnchorWords.csv
'''
file = sys.argv[1]
count = 0
with open('output_corpus.txt', '+a') as outcorp:
	with open('AnchorWords.csv', '+a') as output:
		with open(file) as corpus:
			for lines in corpus:
				#print(lines)
				regex = re.compile(r'\[\[([^\]:;]*?)\]\]', re.S)
				updated_lines = regex.sub(lambda m: m.group().replace(' ', '_'), lines)
				#output.write(updated_lines)
				sub_dictionary = re.findall(r'\[\[([^\];:]*?)[\|]([^\];:]*?)\]\]', updated_lines)
				for elem in sub_dictionary:
					#print(np.array(elem))
					output.write(elem[0]+ ',' + elem[1] + '\n')#saving the output to AnchorWords.csv
					count += 1
					print('Anchor words found: ' + str(count), end= '\r')
					#print(dictionary)
				updated_lines = re.sub(r'\[\[([^\];:]*?)[\|]([^\];:]*?)\]\]', r'\1', updated_lines)
				outcorp.write(updated_lines)

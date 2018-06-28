import sys
import re
import os
import codecs

def upcase_first_letter(s):
	return s[0].upper() + s[1:]

# Replaces the Gensim class LineSentence
class MySentences(object):
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		for root, dirs, files in os.walk(self.dirname):
			for filename in files:
				file_path = root + '/' + filename
				for line in codecs.open(file_path, 'r', encoding='utf-8', errors='ignore'):
					if line == "\n":
						continue
					yield line

def makeDictionary(directory):
	"""
	All the links present in the corpus are treated as resources and
	the text is treated as the surface form for that very entity.
	"""
	counter = 0
	print("Opened ", directory)
	sentences = MySentences(directory)
	dictionary = {}
	for line in sentences:
		counter += 1

		# Finding all the anchor text, that is the <a> tags
		links = re.findall(r'\<a href\=\"([^\"\:]+)\"\>([^\<]+)\</a\>', line)
		for link in links:
			entity = upcase_first_letter(link[0]).replace('%20','_').replace('%28','(').replace('%29',')')
			anchor = link[1].split(' (')[0]
			try:
				dictionary[entity] += ';' + anchor
			except:
				dictionary[entity] = entity
				dictionary[entity] += ';' + anchor
			print("Anchor Text found : " + str(counter), end = '\r')
	with open('../data/AnchorDictionary.csv', '+w') as output:
		for entity in dictionary:
			print('Writing to file: ' + entity, end = '\r')
			output.write(dictionary[entity] + '\n')
	return None

if __name__ == "__main__":
	directory = sys.argv[1]
	makeDictionary(directory)

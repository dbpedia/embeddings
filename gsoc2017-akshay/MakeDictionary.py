import sys
import re
import os

def upcase_first_letter(s):
	return s[0].upper() + s[1:]

class MySentences(object):
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		for root, dirs, files in os.walk(self.dirname):
			for filename in files:
				file_path = root + '/' + filename
				for line in open(file_path):
					if line == "\n":
						continue
					yield line

def makeDictionary(directory):
  #takes about 20 min
	counter = 0
	sentences = MySentences(directory)
	dictionary = {}
	for line in sentences:
		counter += 1
		links = re.findall(r'\<a href\=\"([^\"\:]+)\"\>([^\<]+)\</a\>', line)
		for link in links:
			entity = upcase_first_letter(link[0]).replace('%20','_').replace('%28','(').replace('%29',')')
			anchor = link[1].split(' (')[0]
			#removes the bold and italics wikicode. Also removes trailing parentheses from the anchor text.
			try:
				dictionary[entity] += ';' + anchor
			except:
				dictionary[entity] = entity
				dictionary[entity] += ';' + anchor
			print("Anchor Text found : " + str(counter), end = '\r')
	with open('AnchorDictionary.csv', '+w') as output:
		for entity in dictionary:
			print('Writing to file: ' + entity, end = '\r')
			output.write(dictionary[entity] + '\n')
	return None

if __name__ == "__main__":
	directory = sys.argv[1]
	makeDictionary(directory)

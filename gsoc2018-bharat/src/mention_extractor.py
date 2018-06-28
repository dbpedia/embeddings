import os
import re
import sys
import time
import tempfile
from joblib import Parallel, delayed
from urllib.parse import unquote
from collections import Counter

def upcase_first_letter(s):
	"""
	Capitalize the string.
	"""
    return s[0].upper() + s[1:]

def replaceAnchorText(filename):
	"""
	Given the input file, the surface forms loaded from anchor text
	are used to extract entity mentions and replace them with the
	article title in the text corpus itself.

	Arguments
	---------
	filename : Input file containing the extracted text.
	"""
	print(filename)

	# A temporary file to track the input file document by document.
	t = tempfile.NamedTemporaryFile(mode = "r+")
	dictionary = {}
	with open(filename, 'r') as fil:
		for line in fil:
			if line.startswith("<doc"):
				t.write(line)

				# Get the title of the document from XML
				title = line.split('title="')[1].split('">')[0]
				TITLE = title.replace(' ', '_')

				dictionary = {}
				next(fil)

				# Global surface forms dictionary
				global surfForms
				try:
					dictionary[TITLE] = surfForms[TITLE]
				except:
					dictionary[TITLE] = set([title])

				# Gender dictionary from checking persons
				global gender

				try:
					if gender[title] == 'f':
						dictionary[TITLE].add('she'); dictionary[TITLE].add('her'); dictionary[TITLE].add('hers')
					else:
						dictionary[TITLE].add('he'); dictionary[TITLE].add('him'); dictionary[TITLE].add('his')
				except:
					pass

				continue

			# Regular expressions to find and replace anchor text with resource entity
			elif not line == '\n':
				links = re.findall(r'\<a href\=\"([^\"\:]+)\"\>([^\<]+)\</a\>', line)
				for link in links:
					entity = link[0].replace('wikt%3A', ''); entity = entity.replace('wiktionary%3A', '')
					if entity == '':
						entity = link[1]
						
					entity = unquote(entity[0].upper() + entity[1:]).replace(' ', '_')
					anchor = link[1].split(' (')[0]
					anchor = re.escape(anchor)
					if entity not in dictionary:
						dictionary[entity] = set()
					dictionary[entity].add(anchor)
				line = re.sub('<.*?>', '', line)
			for entity in sorted(dictionary, key = len, reverse = True):
				for surfaceForm in sorted(dictionary[entity], key = len, reverse = True):
					try:
						line = re.sub(r"\b(?<![\/\(])%s\b" % surfaceForm, 'resource/' + entity , line, flags = re.IGNORECASE)
					except:
						dictionary[entity].remove(surfaceForm)

			if not line == '\n':
				t.write(line)

	t.seek(0)

	with open(filename, 'w') as output:
		for line in t:
			output.write(line)

	t.close()

	return None

def loadSurfaceForms(filename, most_cmmn):
	"""
	Takes the surface form dictionary as input and
	returns the loaded entities mapped onto their
	most common surface forms.

	Arguments
	---------
	filename : Input dictionary
	most_cmmn : Parameter to decide the most common surface forms
	"""
	surfaceForm = {}
	c = 0
	with open(filename, 'r') as output:
		for line in output:
			c += 1
			print('Loading surface forms: ' + str(int(c*1000/746565)/10) + '%', end = '\r')
			surfaceForm[line.split(';', 1)[0]] = set(x[0] for x in Counter(line.rstrip('\n').split(';', 1)[1].split(';')).most_common(most_cmmn))
	return surfaceForm

def loadDictionary(filename):
	"""
	Loads the entire surface form dictionary from memory
	"""
	surfaceForm = {}
	with open(filename, 'r') as output:
		for line in output:
			try:
				surfaceForm[line.rsplit(';', 1)[0]] = line.rstrip('\n').rsplit(';', 1)[1]
			except:
				pass
	return surfaceForm

def splitFiles(directory):
	"""
	Iterate through the files in the extracted directory
	"""
	names = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			names.append(root + '/' + file)
	flag = False
	for name in names:
		with open(name, 'r') as inp:
			dirname = name + '_'
			os.mkdir(dirname)
			for line in inp:
				if line.startswith('</doc'):
					continue
				elif line.startswith('<doc'):
					filename = upcase_first_letter(line.split('title="')[1].split('">')[0]).replace(' ', '_')
				else:
					with open(dirname + '/' + filename, '+a') as output:
						if not line == '\n':
							output.write(line)
		os.remove(name)
	return None

if __name__ == "__main__":
	directory = sys.argv[1]

	surfForms = loadSurfaceForms("data/AnchorDictionary.csv", 5)
	gender = loadDictionary('data/gender.csv')

	names = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			names.append(root + '/' + file)
	
	Parallel(n_jobs = 8, verbose = 51)(delayed(replaceAnchorText)(name) for name in names)
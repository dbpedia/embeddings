import os
import re
import sys
import shutil
import time
import tempfile
from joblib import Parallel, delayed

def upcase_first_letter(s):
    return s[0].upper() + s[1:]

def replaceAnchorText(filename):
	print(filename)
	#create a temporary file
	t = tempfile.NamedTemporaryFile(mode = "r+")
	dictionary = {}
	with open(filename, 'r') as fil:
		for line in fil:
			if line.startswith("<doc"):
				t.write(line)
				title = next(fil).rstrip('\n').replace(' ', '_')
				dictionary = {}
				# print(title)
				global surfForms
				# print(surfForms)
				if title in surfForms:
					dictionary[title] = surfForms[title]
					# print(surfForms[title])
				else:
					dictionary[title] = [title.replace('_', '')]
				continue
			elif not line == '\n':
				links = re.findall(r'\<a href\=\"([^\"\:]+)\"\>([^\<]+)\</a\>', line)
				for link in links:
					entity = upcase_first_letter(link[0].replace('wikt%3A', '')).replace('%20','_').replace('%28','(').replace('%29',')')
					anchor = link[1].split(' (')[0]
					if entity not in dictionary:
						dictionary[entity] = []
					if anchor not in dictionary[entity]:
						dictionary[entity].append(anchor)
				line = re.sub('<.*?>', '', line)
			for entity in sorted(dictionary, key = len, reverse = True):
				for surfaceForm in sorted(dictionary[entity], key = len, reverse = True):
					try:
						line = re.sub(r"\b%s\b" % surfaceForm, 'dbo:' + entity , line, flags = re.IGNORECASE)
					except:
						# print("Unable to tag: " + surfaceForm + " as " + entity)
						dictionary[entity].remove(surfaceForm)
			if not line == '\n':
				t.write(line)

	t.seek(0)

	with open(filename, 'w') as output:
		for line in t:
			output.write(line)

	t.close()

	return None

def loadDictionary(filename):
	surfaceForm = {}
	with open(filename, 'r') as output:
		for line in output:
			print('Loading surface forms..', end = '\r')
			surfaceForm[line.split(';', 1)[0]] = set(line.rstrip('\n').split(';', 1)[1].split(';'))
	return surfaceForm

def splitFiles(directory):
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
	names = []
	surfForms = loadDictionary("AnchorDictionary.csv")
	for root, dirs, files in os.walk(directory):
		for file in files:
			names.append(root + '/' + file)
	Parallel(n_jobs = 8)(delayed(replaceAnchorText)(name) for name in names)
		# replaceAnchorText(file)

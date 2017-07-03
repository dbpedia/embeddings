import os
import re
import sys
import time
import tempfile
from joblib import Parallel, delayed
from urllib.parse import unquote
from collections import Counter

# def upcase_first_letter(s):
#     return s[0].upper() + s[1:]

def replaceAnchorText(filename):
	print(filename)
	#create a temporary file
	t = tempfile.NamedTemporaryFile(mode = "r+")
	dictionary = {}
	with open(filename, 'r') as fil:
		for line in fil:
			if line.startswith("<doc"):
				t.write(line)
				title = line.split('title="')[1].split('">')[0]
				TITLE = title.replace(' ', '_')
				dictionary = {}
				next(fil)
				# print(title)
				global surfForms
				# print(surfForms)
				try:
					dictionary[TITLE] = surfForms[TITLE]
					# print(surfForms[title])
				except:
					dictionary[TITLE] = set([title])

				global gender

				try:
					if gender[title] == 'f':
						dictionary[TITLE].add('she'); dictionary[TITLE].add('her'); dictionary[TITLE].add('hers')
					else:
						dictionary[TITLE].add('he'); dictionary[TITLE].add('him'); dictionary[TITLE].add('his')
				except:
					pass

				continue
			elif not line == '\n':
				links = re.findall(r'\<a href\=\"([^\"\:]+)\"\>([^\<]+)\</a\>', line)
				for link in links:
					# print(link[0] + '====' +link[1])
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
						# print("Unable to tag: " + surfaceForm + " as " + entity)
						dictionary[entity].remove(surfaceForm)

				# global commonRef

				# for entity in commonRef:
				# 	line = re.sub(r"\b(?<![\/\(])%s\b" % commonRef[entity], 'resource/' + entity , line, flags = re.IGNORECASE)

			if not line == '\n':
				t.write(line)

	t.seek(0)

	with open(filename, 'w') as output:
		for line in t:
			output.write(line)

	t.close()

	return None

def loadSurfaceForms(filename, most_cmmn):
	surfaceForm = {}
	c = 0
	with open(filename, 'r') as output:
		for line in output:
			c += 1
			print('Loading surface forms: ' + str(int(c*1000/7265689)/10) + '%', end = '\r')
			surfaceForm[line.split(';', 1)[0]] = set(x[0] for x in Counter(line.rstrip('\n').split(';', 1)[1].split(';')).most_common(most_cmmn))
	return surfaceForm

def loadDictionary(filename):
	surfaceForm = {}
	with open(filename, 'r') as output:
		for line in output:
			try:
				surfaceForm[line.rsplit(';', 1)[0]] = line.rstrip('\n').rsplit(';', 1)[1]
			except:
				pass
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

	surfForms = loadSurfaceForms("AnchorDictionary.csv", 5)#selecting the top 5 most common anchor text
	# commonRef = loadDictionary("MostCommon.csv")
	gender = loadDictionary('EntityGender.csv')

	names = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			names.append(root + '/' + file)
	
	Parallel(n_jobs = 8, verbose = 51)(delayed(replaceAnchorText)(name) for name in names)
		# replaceAnchorText(file)
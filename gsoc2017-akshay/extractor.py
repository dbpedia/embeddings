import os
import re
import sys
import shutil

# import mediawiki_parser as mp
# extractor.py corpus.xml
'''
Extract dictionary with the anchor text as key and the entities they correspond to as the values.
for example the dictionary has the following entries as the values for the anchor text "Catalyst" as key.
Catalyst : entity::Catalyst_(software), entity::Catalyst_(TV_program), entity::Catalysis, entity::Catalyst_(band), entity::Catalyst
'''
def makeDictionary(fileName):
	counter = 0
	text_seen = set()
	with open(fileName, 'r') as corpus:
		for line in corpus:
			links = re.findall(r'\[\[([^\]:;]*?)\]\]', line)
			for elem in links:
				if elem not in text_seen:
					counter += 1
					print('Anchor text processed: ' + str(counter), end = '\r')
					#print(elem)
					text_seen.add(elem)
	diction = {}
	for elem in text_seen:
		if elem.split('|')[-1] not in diction:
			diction[elem.split('|')[-1]] = []
		diction[elem.split('|')[-1]].append('entity::' + elem.split('|')[0].replace(' ', '_'))
	print('')
	return diction

def extractArticles(fileName):
	section = ''
	counter = 0
	# flag = False
	with open('articleNames', '+w') as articlenames:
		with open(fileName, 'r') as corpus:
			for line in corpus:
				title = re.search(r'<title>([^<]*?)</title>', line)
				if title:
					filename = title.group(1)
					section = ''
					articlenames.write(filename.replace('/', '::') + '\n')
					makeFile(filename, '')
					counter += 1
					print('No. of aticles processed: ' + str(counter), end = '\r')
				if not (line == '\n' or line.startswith('<') or line.startswith(':') or line.startswith('!') or line.startswith(' ') or line.startswith('*') or line.startswith('{') or line.
 startswith('}') or line.startswith('|')):
					section = line
					makeFile(filename, section)
	print('')
					# counter += 1

				# if (line.startswith('      <text') or line.startswith('=')):
				# 	makeFile(filename, section + '\n')
				# 	counter += 1
				# 	section = line.rstrip('\n')
				# elif not (line.startswith(' ') or line.startswith('<')):
				# 	section += ' ' + line.rstrip('\n')
				# elif line.endswith('/text>\n'):
				# 	section += line
				# 	makeFile(filename, section)
				# 	section = ''
	return None

def makeFile(name, article):
	dire = 'output'
	if not os.path.exists(dire):
		# shutil.rmtree(dire)
		os.makedirs(dire)
	name = 'output/' + name.replace('/', '::')
	with open(name, '+a') as output:
		output.write(clearXML(article))
	return None

def clearXML(text):
	# matchTemplate = ['']
	text = re.sub(r'\<([^\>]*?)\>', '', text)
	text = re.sub(r'\{\{([^\{\}]*?)\}\}', '', text)
	text = re.sub(r'\{\{([^\{\}]*?)\}\}', '', text)
	regex = re.compile(r'\[\[([^\]:;]*?)\]\]', re.S)
	text = regex.sub(lambda m: 'entity::' + m.group().split('|')[0].replace(' ', '_').replace(']', '')
		.replace('[', '').replace('/', '::').split('#')[0], text)
	text = re.sub(r'\[([^\]]*?)\]', '', text)
	text = re.sub(r'\=\=(.*?)\=\=', '', text)
	text = text.replace('&quot;', '').replace('&amp;', '').replace('nbsp;', '')
	text = re.sub(r'\&lt\;(.*?)\&gt\;(.*?)\&lt\;\/(\1)\&gt\;', '', text)
	text = re.sub(r'\&lt\;([^\&]*?)\&gt\;', '', text)
	text = text.replace("'''", "").replace("''", "").replace(']', '').replace('[', '')
	text = text.replace('*', '').replace('=', '')
	text = re.sub(r'\{\{(.*?)', '', text)
	return text

'''
Generates dictionary of the outgoing links for an article.
'''
def makeDiceDictionary(fileName):
	diceDict = {}
	count = 0
	with open(fileName, 'r') as corpus:
		baseEntity = ''
		for line in corpus:
			title = re.search(r'<title>([^<]*?)</title>', line)
			if title:
				baseEntity = 'entity::' + title.group(1)
				diceDict[baseEntity] = []
			links = re.findall(r'\[\[([^\]:;]*?)\]\]', line)
			for link in links:
				count += 1
				print('Links processed: ' + str(count), end ='\r')
				diceDict[baseEntity].append('entity::' + link.replace(' ', '_').strip('|')[0].replace('/', '::'))
	print('')
	return diceDict

'''
returns the dice measure of relatedness between two entities
'''
def diceMeasure(entity1, entity2, diceDict):
	commonCount = 0
	for elem1 in diceDict[entity1]:
		for elem2 in diceDict[entity2]:
			if elem1 == elem2:
				commonCount += 1
	return 2 * commonCount / (len(diceDict[entity1]) + len(diceDict[entity2]))
'''
for a given text, returns the most related entity
'''
def findBestMatch(baseEntity, anchorList, diceDict):
	best = 0
	bestMatch = ''
	for elem in anchorList:
		if diceMeasure(elem, baseEntity, diceDict) > best:
			best = diceMeasure(elem, baseEntity, diceDict)
			bestMatch = elem
	return bestMatch
'''
extract individual articles
'''

def replaceAnchor(dicti, diceDict):
	dire = 'updated_text'
	if not os.path.exists(dire):
		# shutil.rmtree(dire)
		os.makedirs(dire)
	with open('articleNames', 'r') as namesList:
		for name in namesList:
			with open('output/' + name.rstrip('\n'), 'r') as articles:
				with open('updated_text/' + name.rstrip('\n'), '+a') as newFile:
					for lines in articles:
						for anchorText in dicti:
							newline = re.sub(anchorText, findBestMatch(name, dicti[anchorText], diceDict)
								, line, flags=re.IGNORECASE)
							newFile.write(newline)
	return None

# def Selector(name, diction):
# 	with open(name, 'r') as file:


file = sys.argv[1]
# alpha = makeDictionary(file)
# for elem in alpha:
# 	for tex in alpha[elem]:
# 		print(elem +' : ' + tex)

anchorDictionary = makeDictionary(file)
extractArticles(file)
diceDictionary = makeDiceDictionary(file)
replaceAnchor(anchorDictionary, diceDictionary)

shutil.rmtree('output/')
import os
import re
import sys
import shutil
import time
import tempfile
from joblib import Parallel, delayed

file = sys.argv[1]

def upcase_first_letter(s):
    return s[0].upper() + s[1:]

def makeDictionary(fileName):
	counter = 0
	diction = {}
	with open(fileName, 'r') as corpus:
		start_time = time.time()
		for line in corpus:
			links = re.findall("\[\[([^\{\}\:\]\[]+)\|([^\{\}\]\[]+)\]\]", line)
			for elem in links:
				counter += 1
				# print('Anchor text processed: ' + str(counter), end = '\r')
				# print(elem)
				entity = upcase_first_letter(elem[0]).replace(' ', '_')
				#Capitalize the first character of the entity and replace the spaces with underscores.
				surfaceForm = elem[1].replace("'''", "").replace("''", "").split(' (')[0]
				#removes the bold and italics wikicode. Also removes trailing parentheses from the anchor text.
				print("Anchor Text found (" + str(int(counter/(time.time() - start_time))) + "/s) : " + str(counter), end = '\r')
				if entity not in diction:
					diction[entity] = []
				if surfaceForm not in diction[entity]:
					diction[entity].append(surfaceForm)
	return diction

def replaceAnchorText(filename):
	print(filename)

	#create a temporary file
	t = tempfile.NamedTemporaryFile(mode = "r+")
	dictionary = {}

	with open(filename, 'r') as fil:
		for line in fil:
			if line.startswith("<doc id"):
				title = next(fil).rstrip('\n')
				# print(title)
				dictionary = {}
				dictionary[title.replace(' ', '_')] = [title]
				continue
			elif not line == '\n':
				links = re.findall(r'\<a href\=\"([^\"\:]+)\"\>([^\<]+)\</a\>', line)
				for link in links:
					entity = upcase_first_letter(link[0]).replace('%20','_').replace('%28','(').replace('%29',')')
					anchor = link[1].split(' (')[0]
					if entity not in dictionary:
						dictionary[entity] = []
					if anchor not in dictionary[entity]:
						dictionary[entity].append(anchor)
			line = re.sub('<.*?>', '', line)
			for entity in dictionary:
				for surfaceForm in sorted(dictionary[entity], key = len, reverse = True):
					try:
						line = re.sub(r"\b%s\b" % surfaceForm,'resource/' + entity, line, flags = re.IGNORECASE)
					except:
						# print("Unable to tag: " + surfaceForm + " as " + entity)
						dictionary[entity].remove(surfaceForm)
			t.write(line)

	t.seek(0)

	with open(filename, 'w') as output:
		for line in t:
			output.write(line)

	t.close()

	return None

def replaceSurfaceForms(filename, dictionary):
	avoid = ['The', 'the', 'a', 'A', '*ʼ']
	with open("updatedWiki", '+w') as output:
		with open(filename, 'r') as corpus:
			title = ''
			entityList = []#stores the entites present in an article as they appear
			for line in corpus:
				if line.startswith('    <title>'):
					title = line.strip('    <title>').rstrip('</title>\n').replace(' ', '_')
					entityList = [title.replace(' ', '_')]#reset the list for every article
				elif not title == '':
					links = re.findall(r"\[\[([^\{\}\:\]\[]+)\]\]", line)
					for link in links:
						entity = upcase_first_letter(link.split('|')[0]).replace(' ', '_')
						if entity not in entityList:
							entityList.append(entity)
							print(entityList[-1])#last appended entity in the list
				for entity in entityList:
					if entity in dictionary:
						for surfForm in dictionary[entity]:
							if surfForm not in avoid:
								try:
									line = re.sub(r"\b%s\b" % surfForm,'resource/' + entity, line, flags = re.IGNORECASE)
								except:
									print("Unable to tag: " + surfForm)
							# print('====' + entity + '====' + surfForm)
				output.write(line)
	return None
if __name__ == "__main__":
	directory = sys.argv[1]
	for root, dirs, files in os.walk(directory):
		start = time.time()
		Parallel(n_jobs = 8)(delayed(replaceAnchorText)(root + '/' + file) for file in files)
		print(str(31*100/(time.time() - start)) + ' articles/s')
		# replaceAnchorText(file)

import os
import re
import sys
import shutil
import time

file = sys.argv[1]

def upcase_first_letter(s):
    return s[0].upper() + s[1:]

def makeDictionary(fileName):
	counter = 0
	diction = {}
	with open(fileName, 'r') as corpus:
		start_time = time.time()
		for line in corpus:
			links = re.findall("\[\[([^\{\}\:\]\[]+)\|([^\{\}\]\[]+)\]\]", line, re.DOTALL | re.UNICODE)
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
	counter = 0
	avoid = ['The', 'the', 'a', 'A', '*ʼ']
	with open("updatedWiki", '+w') as output:
		with open(filename, 'r') as corpus:
			title = ''
			localDictionary = {}#stores the entites and present in an article as they appear
			for line in corpus:
				if line.startswith('    <title>'):
					title = line.strip('    <title>').rstrip('</title>\n')
					counter += 1
					print("Articles processed: " + str(counter), end = '\r')
					localDictionary = {}#reset the local dictionary for every article
					localDictionary[title.replace(' ', '_')] = [title]
				elif not title == '':
					links = re.findall(r"\[\[([^\{\}\:\]\[]+)\|([^\{\}\]\[]+)\]\]", line)
					for link in links:

						entity = upcase_first_letter(link[0]).replace(' ', '_')
						surfaceForm = link[1].replace("'''", "").replace("''", "").split(' (')[0]

						if entity not in localDictionary:
							localDictionary[entity] = []
						if surfaceForm not in localDictionary[entity]:
							localDictionary[entity].append(surfaceForm)
					singleLinks = re.findall(r"\[\[([^\{\}\:\]\[\|]+)\]\]", line)

					for link in singleLinks:

						entity = upcase_first_letter(link).replace(' ', '_').replace("'''", "").replace("''", "")
						surfaceForm = link.replace("'''", "").replace("''", "").split(' (')[0]

						if entity not in localDictionary:
							localDictionary[entity] = []
						if surfaceForm not in localDictionary[entity]:
							localDictionary[entity].append(surfaceForm)

				# line = re.sub(r"\[\[([^\{\}\:\]\[]+)\|([^\{\}\]\[]+)\]\]", "entity/" + upcase_first_letter(r"\1").replace(' ', '_'), line)
				# line = re.sub(r"\[\[([^\{\}\:\]\[\|]+)\]\]", "entity/" + upcase_first_letter(r"\1").replace(' ', '_'), line)

				for entity in localDictionary:
					for surfForm in localDictionary[entity]:
						if surfForm not in avoid:
							try:
								line = re.sub(r"\b%s\b" % surfForm,'entity/' + entity, line, flags = re.IGNORECASE)
							except:
								pass
							# print('====' + entity + '====' + surfForm)
				output.write(line)
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
								line = re.sub(r"\b%s\b" % surfForm,'resource/' + entity, line, flags = re.IGNORECASE)
							# print('====' + entity + '====' + surfForm)
				output.write(line)
	return None

replaceAnchorText(file)

import sys
import re
from numpy.random import choice
import numpy as np
import os
import time
# leng = 6
# dim = 600
# q = 1./120

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext

def randomVector(num):
	q = 1./120
	return choice([-1, 0, 1], size=num, p=[q/2, 1-q, q/2])

def add(vec1, vec2):
	return np.add(vec1, vec2)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        punct = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'
        for root, dirs, files in os.walk(self.dirname):
            for filename in files:
                file_path = root + '/' + filename
                for line in open(file_path):
                    sline = line.strip()
                    if sline == "":
                        continue
                    rline = cleanhtml(sline)
                    yield re.sub(r'[%s]' % punct, '', re.sub(r'resource/', '', rline)).lower().split()

def generateEmbeddings(filename):
	words = set()
	leng = 6
	dim = 600
	now = time.time()
	count = 0
	global embeddings
	global index
	with open(filename, 'r') as corpus:
		for sentence in corpus:
			if len(sentence) >= leng:
				for i in range(len(sentence) - leng):
					if sentence[i] not in words:
						embeddings[sentence[i]] = np.zeros(dim)
						words.add(sentence[i])
					for j in range(int(i - leng/2), i):#left context
						try:
							embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]])
						except:
							index[sentence[j]] = randomVector(dim)
							embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]])
					for j in range(i + 1, int(i + (leng/2) + 1)):#right context
						try:
							embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]])
						except:
							index[sentence[j]] = randomVector(dim)
							embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]])
					# print(sentence[i] + '(' + str(embeddings[sentence[i]]) + ')')
					# print(sentence[i], end=' ')
					count += 1
					print(str(count/(time.time() - now)) + 'words/s', end = '\r')
	with open('embedding s', 'w+') as output:
		for word in embeddings:
			output.write(word + ';' + str(embeddings[word]) + '\n')
	with open('index', 'w+') as output:
		for word in index:
			output.write(word + ';' + str(index[word]) + '\n')
	return embeddings, index, words

if __name__ == '__main__':
	directory = sys.argv[1]
	embeddings = {}
	index = {}
	names = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			names.append(root + '/' + file)
	for filename in names:
		generateEmbeddings(filename)
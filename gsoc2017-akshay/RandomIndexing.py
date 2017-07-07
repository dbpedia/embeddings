import sys
import re
from numpy.random import choice
import numpy as np
import os
from multiprocessing import Process, Manager
# leng = 6
# dim = 600
# q = 1./120

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext

def tok(txt):
	if txt.startswith('<'):
		return []
	punct = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'
	return re.sub(r'[%s]' % punct, '', re.sub(r'resource/', '', txt)).lower().split()


def randomVector(num):
	q = 1./120
	return choice([-1, 0, 1], size=num, p=[q/2, 1-q, q/2])

def add(vec1, vec2):
	return np.add(vec1, vec2)

def generateEmbeddings(index, embeddings, filename):
	leng = 10
	dim = 600#vector dimens
	print('START: ', str(os.getpid()), 'FILE: ', filename)
	with open(filename, 'r') as corpus:
		for sentences in corpus:
			sentence = tok(sentences)
			if len(sentence) >= leng:
				for i in range(len(sentence) - leng):
					try:
						embeddings[sentence[i]]
					except:
						embeddings[sentence[i]] = np.zeros(dim)
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
	print('COMPLETE: ', str(os.getpid()), 'FILE: ', filename)

if __name__ == '__main__':
	directory = sys.argv[1]
	# embeddings = {}
	# index = {}
	filenames = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			filenames.append(root + '/' + file)


	manager = Manager()
	embeddings = manager.dict()
	index = manager.dict()


	proc = [Process(target=generateEmbeddings, args=(index, embeddings, file)) for file in filenames]
	for p in proc: p.start()
	for p in proc: p.join()

	embeddings = dict(embeddings)
	index = dict(index)

	with open('embeddings', 'w+') as output:
		for word in embeddings:
			output.write(word + ' ==')
			for i in embeddings[word]:
				output.write(' ' + str(int(i)))
			output.write('\n')

	with open('index', 'w+') as output:
		for word in index:
			output.write(word + ' ==')
			for i in index[word]:
				output.write(' ' + str(int(i)))
			output.write('\n')

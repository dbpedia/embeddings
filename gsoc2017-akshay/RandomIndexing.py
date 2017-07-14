import sys
import re
from numpy.random import choice
import numpy as np
import os
from multiprocessing import Process, Manager, Pool
import time
# leng = 6
# dim = 600
# q = 1./120

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        punct = '!"#$%&\'()*+,.:;<=>?@[\\]^`{|}~'
        for root, dirs, files in os.walk(self.dirname):
            for filename in files:
                file_path = root + '/' + filename
                for line in open(file_path):
                    sline = line.strip()
                    if sline == "":
                        continue
                    rline = cleanhtml(sline)
                    yield re.sub(r'[%s]' % punct, '', rline).lower().split()


def randomVector(num):
	q = 1./30
	return choice([0, 1], size=num, p=[1 - q, q])

def add(vec1, vec2):
	return np.add(vec1, vec2)

def generateEmbeddings(index, embeddings, sentence, wc):
	leng = 10
	dim = 300#vector dimens
	# print('START: ', str(os.getpid()), 'FILE: ', filename)
	# with open(filename, 'r') as corpus:
	if len(sentence) >= leng:
		for i in range(len(sentence) - leng):
			if sentence[i].startswith("resource/"):
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

	print("Processed ", str(wc), " words.", end="\r")
			# print(sentence[i] + '(' + str(embeddings[sentence[i]]) + ')')
			# print(sentence[i], end=' ')

if __name__ == '__main__':
	directory = sys.argv[1]
	# embeddings = {}
	# index = {}
	sentences = MySentences(directory)
	manager = Manager()
	embeddings = manager.dict()
	index = manager.dict()
	wc = 0
	now = time.time()

	pool = Pool(processes=6)
	for sentence in sentences:
		wc += len(sentence)
		pool.apply_async(generateEmbeddings, args=(index, embeddings, sentence, wc))
	pool.close()
	pool.join()

	print("Processed ", str(wc), " words.")

	print("Time elapsed: ", str(time.time() - now), 's')

	embeddings = dict(embeddings)
	index = dict(index)

	with open('embeddings', 'w+') as output:
		with open('labels', 'w+') as op:
			for word in embeddings:
				# output.write(word + ' ==')
				op.write(word + '\n')
				for i in embeddings[word]:
					output.write(' ' + str(i))
				output.write('\n')

	with open('index', 'w+') as output:
		for word in index:
			output.write(word + ' ==')
			for i in index[word]:
				output.write(' ' + str(int(i)))
			output.write('\n')

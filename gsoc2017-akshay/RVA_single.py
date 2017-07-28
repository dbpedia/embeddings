import sys
import re
import numpy as np
import os
import time
from random import random
import shelve

def rand(minimum, maximum):
	return minimum + (maximum - minimum) * random()

class Sparse:
	def __init__(self, dim, count, limit):
		self.dim = dim
		self.sparse = {}
		for i in range(count):
			self.sparse[int(rand(0, dim))] = rand(-limit, limit)
#dim = dimension of vector
#count = number of non-zero values
#limit = range of the non-zero values

	def value(self):
		a = []
		for i in range(self.dim):
			try:
				a.append(self.sparse[i])
			except:
				a.append(0)
		return a

def add(a, b, weight=1):
	c = a
	for i in b.sparse:
		try:
			c.sparse[i] += (weight * b.sparse[i])
		except:
			c.sparse[i] = (weight * b.sparse[i])
	return c

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
				print(file_path)
				for line in open(file_path):
					sline = line.strip()
					if sline == "":
						continue
					if sline.startswith('<doc'):
						sline = 'title/resource/' + sline.split('title="')[1].split('">')[0].replace(' ', '_')
					rline = cleanhtml(sline)
					yield re.sub(r'[%s]' % punct, '', rline).lower().split()

if __name__ == '__main__':
	directory = sys.argv[1]
	sentences = MySentences(directory)
	wc = 0
	title = ''
	now = time.time()
	dim = 500#vector dimension
	window = 6#window for context words
	count = 2#number of non-zero values
	limit = 5#range of non-zero values
	wt = 1

	# pool = Pool()
	index = shelve.open('index.db')
	embeddings = {}#shelve.open('embeddings.db')
	for sentence in sentences:
		wc += len(sentence)
		if len(sentence) > 0 and sentence[0].startswith('title/'):
			title = sentence[0].split('title/')[1]
			# print(title)
			# generateEmbeddings(index, embeddings, sentence, title)
		try:
			index[title]
		except:
			index[title] = Sparse(dim, count, limit)

		if len(sentence) > window:
			for i in range((window / 2), len(sentence) - window / 2):
				if sentence[i].startswith("resource/"):
					#add index vector of title entity
					try:
						embeddings[sentence[i]] = add(embeddings[sentence[i]], index[title], 7)
					except:
						embeddings[sentence[i]] = Sparse(dim, 0, 1)
						embeddings[sentence[i]] = add(embeddings[sentence[i]], index[title], 7)

					#neighbouring words
					for j in range(int(i - window/2), i):#left context
						if sentence[j].startswith("resource/"):
							wt = 5#weight for context entities
						else:
							wt = 1#weight for non-entity words
						try:
							embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
						except:
							index[sentence[j]] = Sparse(dim, count, limit)
							embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
					for j in range(i + 1, int(i + (window/2) + 1)):#right context
						if sentence[j].startswith("resource/"):
							wt = 5
						else:
							wt = 1
						try:
							embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
						except:
							index[sentence[j]] = Sparse(dim, count, limit)
							embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
	index.close()
	# embeddings.close()
	print("Processed ", str(wc), " words.")

	print("Time elapsed: ", str(time.time() - now), 's')

	with open('embeddings', 'w+') as output:
		with open('labels', 'w+') as op:
			for word in embeddings.keys():
				# output.write(word + ' ==')
				op.write(word + '\n')
				for i in embeddings[word].value():
					output.write(' ' + str(i))
				output.write('\n')

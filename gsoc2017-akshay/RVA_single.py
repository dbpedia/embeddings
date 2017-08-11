import sys
import re
import numpy as np
import os
import time
from random import random
import shelve
# from sqlite_object import SqliteDict

def rand(minimum, maximum):
	return minimum + (maximum - minimum) * random()

def tok(line):
	punct = '!"#$%&\'()*+,.:;<=>?@[\\]^`{|}~'
	sline = line.strip()
	if sline == "":
		return []
	if sline.startswith('<doc'):
		try:
			sline = 'title/resource/' + sline.split('title="')[1].split('">')[0].replace(' ', '_')
		except:
			sline = 'title/err'
			print(line)
	#rline = cleanhtml(sline)
	return re.sub(r'[%s]' % punct, '', sline).lower().split()
# class Sparse:
# 	def __init__(self, dim, count, limit):
# 		self.dim = dim
# 		self.sparse = np.zeros(dim)
# 		for i in range(count):
# 			self.sparse[int(rand(0, dim))] = rand(-limit, limit)
# 	def value(self):
# 		return self.sparse
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
		a = np.zeros(self.dim)
		for i in self.sparse:
			a[i] = self.sparse[i]
		return a

def add(a, b, weight=1):
	#a is an np array
	#b is the sparse array
	return (b.value() * weight) + a

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
				print('______________________', file_path, '____________________')
				for line in open(file_path):
					sline = line.strip()
					if sline == "":
						continue
					if sline.startswith('<doc '):
						try:
							sline = 'title/resource/' + sline.split('title="')[1].split('">')[0].replace(' ', '_')
						except:
							sline = 'title/err'
							print(filename, line)
					rline = cleanhtml(sline)
					yield re.sub(r'[%s]' % punct, '', rline).lower().split()

if __name__ == '__main__':
	directory = sys.argv[1]
	sentences = MySentences(directory)
	wc = 0
	now = time.time()
	title = ''
	dim = 500#vector dimension
	window = 10#window for context entities
	win = 2#window for context words
	count = 2#number of non-zero values
	limit = 5#range of non-zero values
	wt = 1
	counter = 0
	prog = 0

	# pool = Pool()
	# index = shelve.open('index.db', writeback=True)
	index = {}
	index['err'] = Sparse(dim, 0, 1)
	# embeddings = shelve.open('embeddings.db', writeback=True)
	embeddings = {}
	filenames = []
	for root, dirs, files in os.walk(directory):
		for fil in files:
			filenames.append(root + '/' + fil)
	filenames = sorted(filenames)

	for filename in filenames:
		# if counter < 2000:
		# counter += 1
		prog += 1
		print(str(prog*100./14800) + '%', filename)
		with open(filename, 'r') as corpus:
			for sentences in corpus:
				sentence = tok(sentences)
				wc += len(sentence)
				#print(sentence)

				if len(sentence) > 0 and sentence[0].startswith('title/'):
					title = sentence[0].split('title/')[1]
					# print(title)
					try:
						index[title]
					except:
						index[title] = Sparse(dim, count, limit)

				if len(sentence) > window:
					for i in range((window / 2), len(sentence) - window / 2):
						if sentence[i].startswith("resource/"):
							#add index vector of title entity
							titlewt = 7
							try:
								embeddings[sentence[i]] = add(embeddings[sentence[i]], index[title], titlewt)
							except:
								# embeddings[sentence[i]] = Sparse(dim, 0, 1)
								embeddings[sentence[i]] = np.zeros(dim)
								embeddings[sentence[i]] = add(embeddings[sentence[i]], index[title], titlewt)

							#neighbouring words
							for j in range(int(i - window/2), i):#left context
								if sentence[j].startswith("resource/"):
									wt = 5#weight for context entities
									try:
										embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
									except:
										index[sentence[j]] = Sparse(dim, count, limit)
										embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
								elif j >= int(i - win/2):
									wt = 1
									try:
										embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
									except:
										index[sentence[j]] = Sparse(dim, count, limit)
										embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)


							for j in range(i + 1, int(i + (window/2) + 1)):#right context
								if sentence[j].startswith("resource/"):
									wt = 5
									try:
										embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
									except:
										index[sentence[j]] = Sparse(dim, count, limit)
										embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
								elif j <= int(i + win/2):
									wt = 1
									try:
										embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)
									except:
										index[sentence[j]] = Sparse(dim, count, limit)
										embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]], wt)

		# if counter == 2000:
		# 	print('Till ' + filename)#inclusive
		# 	print('Updating..')
		# 	counter = 0
		# 	nam = 'embed_till_' + filename.replace('/', '_')
		# 	embed = shelve.open(nam, writeback=True)
		# 	embed.update(embeddings)
		# 	# for key in embeddings.keys():
		# 	# 	try:
		# 	# 		embed[key] = add(embed[key], embeddings[key])
		# 	# 	except:
		# 	# 		embed[key] = embeddings[key]
		# 	embed.close()
		# 	print('Updated.', str(time.time() - now), 's')
		# 	embeddings = {}
	embed = shelve.open('embeddings.db')
	embeddings.update(embeddings)
	embed.close()
	# embeddings.close()
	# nam = 'embed_till_' + filename.replace('/', '_')
	# embed = shelve.open(nam, writeback=True)
	# for key in embeddings.keys():
	# 	try:
	# 		embed[key] = add(embed[key], embeddings[key])
	# 	except:
	# 		embed[key] = embeddings[key]
	# embed.close()
	# embeddings.close()
	print("Processed ", str(wc), " words.")

	print("Time elapsed: ", str(time.time() - now), 's')
	ind = shelve.open('index.db')
	ind.update(index)
	ind.close()

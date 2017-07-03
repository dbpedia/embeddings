import gensim
import logging
import multiprocessing
import os
import re
import sys
from time import time

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext

class MyArticles(object): 
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		punct = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'
		sline = ''
		for root, dirs, files in os.walk(self.dirname):
			for filename in files:
				file_path = root + '/' + filename
				for line in open(file_path):
					if line.startswith('<doc'):
						yield re.sub(r'[%s]' % punct, '', re.sub(r'resource/', '', sline)).lower().split()
						sline = ''
					sline += cleanhtml(line.strip('\n') + ' ')

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
                    yield re.sub(r'[%s]' % punct, '', rline).lower().split()


data_path = sys.argv[1]
begin = time()

# sentences = MySentences(data_path)
sentences = MyArticles(data_path)
model = gensim.models.Word2Vec(sentences, size=300, window=10, min_count=10, workers=6)

model.save("word2vec_gensim")
print("Total procesing time: %d seconds" % (time() - begin))
model.wv.save_word2vec_format("word2vec_org", "vocab", binary=False)
print("Total procesing time: %d seconds" % (time() - begin))
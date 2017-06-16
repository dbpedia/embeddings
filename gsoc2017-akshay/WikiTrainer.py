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


data_path = sys.argv[1]
begin = time()

sentences = MySentences(data_path)
model = gensim.models.Word2Vec(sentences, size=200, window=10, min_count=10, workers=multiprocessing.cpu_count())

model.save("model/word2vec_gensim")
model.wv.save_word2vec_format("model/word2vec_org", "model/vocab", binary=False)
print("Total procesing time: %d seconds" % (time() - begin))

import sys
import re
# from numpy.random import choice
import numpy as np
import os
from multiprocessing import Process, Manager, Pool
import time
# window = 6
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
                    if sline.startswith('<doc'):
                        sline = 'title/resource/' + sline.split('title="')[1].split('">')[0].replace(' ', '_')
                    rline = cleanhtml(sline)
                    yield re.sub(r'[%s]' % punct, '', rline).lower().split()

#using numpy
# def randomVector(num):
#   q = 1./30
#   return choice([0, 1], size=num, p=[1 - q, q])

# generate sparse random vectors fast using time.time()
def randomVector(dim):
    rv = np.zeros(dim)
    for i in range(10):
        rv[int(time.time()*10000000)%dim] = (time.time()*10000000)%10
    return rv

#using fastrand
# def randomVector(dim):
#   rv = np.zeros(dim)
#   for i in range(10):
#       rv[fastrand.pcg32bounded(dim)] = fastrand.pcg32bounded(5)
#   return rv

def add(vec1, vec2, weight=1):
    return np.add(vec1, weight * vec2)

def generateEmbeddings(index, embeddings, sentence, title):
    dim = 5000#vector dimens
    window = 2#widnow for context words
    try:
        index[title]
    except:
        index[title] = randomVector(5000)

    if len(sentence) >= window:
        for i in range(len(sentence) - window):
            if sentence[i].startswith("resource/"):
                #add index vector of title entity
                try:
                    embeddings[sentence[i]] = add(embeddings[sentence[i]], index[title], 3)
                except:
                    # embeddings[sentence[i]] = np.zeros(dim)
                    embeddings[sentence[i]] = 3 * index[title]

                #neighbouring words
                for j in range(int(i - window/2), i):#left context
                    try:
                        embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]])
                    except:
                        index[sentence[j]] = randomVector(dim)
                        embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]])
                for j in range(i + 1, int(i + (window/2) + 1)):#right context
                    try:
                        embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]])
                    except:
                        index[sentence[j]] = randomVector(dim)
                        embeddings[sentence[i]] = add(embeddings[sentence[i]], index[sentence[j]])


    # print("Processed ", str(wc), " words.", end="\r")
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
    title = ''

    # proc = [Process(target=generateEmbeddings, args=(index, embeddings, file)) for file in filenames]
    # for p in proc: p.start()
    # for p in proc: p.join()
    now = time.time()

    pool = Pool()
    for sentence in sentences:
        wc += len(sentence)
        if len(sentence) > 0 and sentence[0].startswith('title/'):
            print(sentence)
            title = sentence[0].split('title/')[1]
        else:
            pool.apply_async(generateEmbeddings, args=(index, embeddings, sentence, title))
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
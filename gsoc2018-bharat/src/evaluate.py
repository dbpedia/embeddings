import numpy as np
from numpy.linalg import norm
import json
from gensim.models import FastText
import logging
import sys
import torch
import Encoder
from torch.autograd import Variable
from sklearn.metrics.pairwise import cosine_similarity


logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO
punctuation = '!"#$%&\'()*+,.:;<=>?@[\\]^`{|}~'
table = str.maketrans('', '', punctuation)
dictionary = {}
model = FastText.load('model/entity_fasttext_n100')
wv = model.wv
del model


def load_dictionary(dictionary_file):
    """
    Load the dictionary with article titles mapped
    to their respective abstracts containing annotated
    text.

    Argument
    --------
    dictionary_file: Input file
    """
    global dictionary
    logging.info('loading saved abstracts from {0}'.format(dictionary_file))
    with open(dictionary_file, 'r') as f:
        for line in f:
            j = json.loads(line)
            dictionary.update(j)


def load_db(db_file):
    """
    Load the saved embeddings database

    Argument
    --------
    db_file: JSON file with computed embeddings
    """
    db = {}
    logging.info('loading weighted vectors from {0}'.format(db_file))
    with open(db_file, 'r') as f:
        for line in f:
            j = json.loads(line)
            db.update(j)
            return db


def mean_encoder(description):
    """
    Encodes the description using simple vector averaging

    Argument
    --------
    description: Description that is to be encoded
    """
    global wv, table
    d = description.translate(table).lower().split()
    r = np.array(list(map(lambda x: wv.get_vector(x), d)),
                 dtype=np.float32)
    return r.mean(axis=0)


def distance_encoder(description):
    """
    Encodes the description using simple vector averaging

    Argument
    --------
    description: Description that is to be encoded
    """
    global wv, table
    d = description.translate(table).lower().split()
    r = list(map(lambda x: wv.get_vector(x), d))
    r = np.array([idx / (i + 1) for i, idx in enumerate(r)],
                 dtype=np.float32)
    return r.mean(axis=0)


def title_mean(label):
    """
    Generates the embedding by averaging the vectors
    representing the words present in the title

    Argument
    --------
    title: Title/Label of the entity
    """
    global wv, table
    label = label.translate(table).lower().replace('_', ' ').split()
    r = np.array(list(map(lambda x: wv.get_vector(x), label)),
                 dtype=np.float32)
    return r.mean(axis=0)


def abstract_encoder(label):
    """
    Encodes the abstract using the RNN network

    Argument
    --------
    dictionary: Dictionary containing all abstracts
    label: Label for the entity that is to be encoded
    """
    global dictionary, wv, table
    model = torch.load('model/description_encoder')
    # label = label.lower()
    try:
        abstract = dictionary[label]
        d = abstract.translate(table).lower()
        d = d.replace('resource/', '').split()
        r = np.array(list(map(lambda x: wv.get_vector(x), d)),
                     dtype=np.float32)
        hidden = model.init_hidden()
    except KeyError:
        return np.random.randn(100)
    try:
        for word in r:
            p, hidden = model(Variable(torch.tensor([[word]])),
                              hidden)
            p = p[0][0].detach().numpy()
        return p
    except (KeyError, IndexError, TypeError) as _:
        return np.random.randn(100)


def print_summary(s):
    print("INFO : Summary")
    print("=" * 40)
    print("Mean vector\t\t|\t{0:.3f}".format(s[0]))
    print("Mean distance vector\t|\t{0:.3f}".format(s[1]))
    print("Mean title vector\t|\t{0:.3f}".format(s[2]))
    print("Encoded vector\t\t|\t{0:.3f}".format(s[3]))
    print("Random vector\t\t|\t{0:.3f}".format(s[4]))
    print("Zero vector\t\t|\t{0:.3f}".format(s[5]))


def evaluate():
    global dictionary, wv
    count = 0
    scores = np.zeros(6)
    itr = len(dictionary)
    logging.info('running evaluation for {0} samples'.format(itr))
    for key in dictionary:
        progress = (count / itr) * 100
        d = dictionary[key].split('resource/')
        d = [idx.split()[0].translate(table).lower() for idx in d[1:]]
        try:
            r = np.array(list(map(lambda x: wv.get_vector(x), d)),
                         dtype=np.float32)
        except KeyError:
            itr -= 1
            continue
        if np.any(np.isnan(r)):
            itr -= 1
            continue
        else:
            if r.ndim == 2:
                try:
                    r = r.mean(axis=0).reshape(1, -1)
                    mean_vec = mean_encoder(dictionary[key]).reshape(1, -1)
                    mean_dist_vec = distance_encoder(dictionary[key]).reshape(1, -1)
                    title_vec = title_mean(key).reshape(1, -1)
                    abstract_vec = abstract_encoder(key).reshape(1, -1)
                    random_vec = np.random.randn(100).reshape(1, -1)
                    zero_vec = np.zeros(100).reshape(1, -1)
                    scores[0] += norm(r - mean_vec)
                    scores[1] += norm(r - mean_dist_vec)
                    scores[2] += norm(r - title_vec)
                    scores[3] += norm(r - abstract_vec)
                    scores[4] += norm(r - random_vec)
                    scores[5] += norm(r - zero_vec)
                    count += 1
                except (ValueError, KeyError) as _:
                    itr -= 1
                    continue
            else:
                itr -= 1
                continue
    scores = scores / norm(scores)
    print_summary(scores)


def main():
    dictionary_file = sys.argv[1]
    load_dictionary(dictionary_file)
    evaluate()


if __name__ == '__main__':
    main()

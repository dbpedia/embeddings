import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import json
from gensim.models import FastText
import logging
import sys

torch.manual_seed(1)

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO


def load_model(saved_model):
    """
    Load the saved model containing
    pre-trained embeddings. I deleted
    the model while just keeping the
    vectors to save memory.
    """
    model = FastText.load(saved_model)
    wv = model.wv
    del model
    return wv


def load_mappings(descriptions, wv):
    """
    Input to an LSTM must be a 3D tensor. For that, I
    am reading all the descriptions line by line and
    storing their embeddings row wise into a numpy
    array of 3 dimensions and shape (n, 500, 300).
    """
    count = 0

    # Fixed shape for the input layer of the lstm network.
    shape = (500, 300)
    entities = []
    abstracts = []
    with open(descriptions, 'r') as input_file:
        logging.info('mapping the resources and their descriptions')
        for line in input_file:
            if count % 5000 == 0:
                logging.info('reading resource # {0}'.format(count))
            json_line = json.loads(line)

            # Resource is extracted
            ent = [_ for _ in json_line.keys()][0]

            # Description is extracted and split into tokens
            desc = json_line[ent].split()
            try:
                # Using a temporary array to pad the original embedding
                # can be replaced by np.pad()
                t = np.zeros(shape, dtype=np.float32)
                v = np.array(wv.get_vector(ent), dtype=np.float32)
                r = np.array(list(map(lambda x: wv.get_vector(x), desc)),
                             dtype=np.float32)

                # Padding the array to a fixed shape.
                t[:r.shape[0], :r.shape[1]] = r
                entities.append(v)
                abstracts.append(t)
                count += 1
            except KeyError:
                continue
    logging.info('resources read into np stack of length : {0}'.format(count))

    # Currently the process is killed here because of memory pressure.
    entities = np.stack(entities)
    abstracts = np.stack(abstracts)
    logging.info('saving entity embeddings to data/entity.npy')
    np.save('../data/entity.npy', entities)
    logging.info('saving description embeddings to data/description.npy')
    np.save('../data/description.npy', abstracts)


def create_tensors():
    pass


def main(saved_model, descriptions_file):
    wv = load_model(saved_model)
    load_mappings(descriptions_file, wv)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'save':
        saved_model, descriptions_file = sys.argv[2], sys.argv[3]
        main(saved_model, descriptions_file)
    elif mode == 'load':
        create_tensors()

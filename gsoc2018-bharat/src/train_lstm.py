import torch
import torch.autograd as autograd
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import numpy as np
import json
from gensim.models import FastText
from gensim.models import KeyedVectors
import logging
import sys
import argparse
import matplotlib.pyplot as plt

from Encoder import DescriptionEncoder

torch.manual_seed(1)

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO
punctuation = '!"#$%&\'()*+,.:;<=>?@[\\]^`{|}~'
table = str.maketrans('', '', punctuation)


def create_mappings(saved_model_file, saved_descriptions_file):
    """
    Input to an LSTM must be a 3D tensor. For that, I
    am reading all the descriptions line by line and
    storing their embeddings row wise into a numpy
    array of 3 dimensions and shape (batch_size, seq_len, embed_size).
    """
    count = 0
    saved_model = saved_model_file
    descriptions_file = saved_descriptions_file
    # wv = KeyedVectors.load_word2vec_format(saved_model, binary=False)
    model = FastText.load(saved_model)
    wv = model.wv
    del model

    # Fixed shape for the input layer of the lstm network.
    shape = (500, 100)
    entities = []
    abstracts = []
    lines = []
    with open(descriptions_file, 'r') as input_file:
        logging.info('mapping the resources and their descriptions')
        for line in input_file:
            if count % 10000 == 0:
                logging.info('reading resource # {0}'.format(count))

            # Read the entire dictionary in first pass
            json_line = json.loads(line)
            lines.append(json_line)
            count += 1

    for l in lines:
        ent = [_ for _ in l.keys()][0]
        desc = l[ent].translate(table).replace('resource/', '').split()
        if len(desc) > 10:
            try:
                d = np.array(list(map(lambda x: wv.get_vector(x), desc)),
                             dtype=np.float32)
                e = np.array(wv.get_vector(ent.replace('resource/', '')),
                             dtype=np.float32)
                entities.append(e)
                abstracts.append(d)
            except (IndexError, KeyError) as _:
                continue


    logging.info(f'{len(abstracts)} mappings generated')

    return abstracts, entities, wv


def load_tensors(directory):
    """
    Input to an LSTM must be a 3D tensor. For that, I
    am reading all the descriptions line by line and
    storing their embeddings row wise into a numpy
    array of 3 dimensions and shape (n, 200, 100).
    """
    logging.info('loading saved embeddings')
    X = np.load(directory + '/description.npy')
    y = np.load(directory + '/entity.npy')
    logging.info('loaded {0} saved embeddings'.format(len(X)))
    train(X, y)


def train(x, y, wv, model, epochs, abstracts_file):
    """
    This method takes the inputs, and the labels
    and trains the LSTM network to predict the
    embeddings based on the input sequnce.

    Arguments
    ---------
    x : List of input descriptions
    y : List of target entity embeddings
    wv : Keyed Word Vectors for pre-trained embeddings
    """
    # epochs = 100
    # embed_size = 100
    # hidden_size = 50
    # seq_len = 1
    # num_layers = 2
    inputs = x
    labels = y
    itr = len(inputs)
    progress = 0.0
    criterion = nn.CosineEmbeddingLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.2)
    count = 0
    itr_p = 0.0
    loss = 0
    losses = np.zeros(epochs)
    logging.info('training on {0} samples'.format(itr))
    for epoch in range(epochs):
        logging.info(
            'starting epoch {0}'.format(epoch + 1))
        flags = Variable(torch.ones(1))
        count = 0
        hidden = model.init_hidden()
        for i, l in zip(inputs, labels):
            count += 1
            progress = (count / itr) * 100
            print('INFO : PROGRESS : {0:.1f} %'.format(progress), end='\r')
            for word in i:
                output, hidden = model(
                    Variable(torch.tensor([[word]])),
                    hidden)
            optimizer.zero_grad()
            loss = criterion(output[0],
                             Variable(torch.tensor([l])),
                             flags)
            loss.backward(retain_graph=True)
            optimizer.step()
        logging.info(
            'completed epoch {0}, loss : {1}'.format(epoch + 1, loss.item()))
        losses[epoch] = loss.item()
    logging.info('saving the model to model/description_encoder')
    torch.save(model, 'model/description_encoder')
    validate(model, wv, abstracts_file)
    plt.plot(losses)
    plt.title('Model Loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.show()


def validate(model, wv, abstracts_file):
    shape = (500, 100)

    with open(abstracts_file, 'r') as input_file:
        with open('data/validate_output', 'w+') as output_file:
            for line in input_file:
                json_line = json.loads(line)
                target = [_ for _ in json_line.keys()][0]
                d = json_line[target]
                desc = json_line[target].translate(table).split()
                if len(desc) > 10:
                    try:
                        r = np.array(list(map(lambda x: wv.get_vector(x),
                                              desc)),
                                     dtype=np.float32)
                    except KeyError:
                        continue
                    hidden = model.init_hidden()
                    for word in r:
                        try:
                            p, hidden = model(Variable(torch.tensor([[word]])),
                                              hidden)
                            p = p[0][0].detach().numpy()
                        except (TypeError, IndexError) as _:
                            continue
                    print('Entity : ' + target)
                    print('Abstract : ' + d, end='')
                    print('Predicted : ', end='')
                    print(wv.similar_by_vector(p))
                    output_file.write(target + '\n')
                    output_file.write(d)
                    output_file.write(str(p) + '\n')
                    break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default="model/entity_fasttext_n100",
                        help="saved pre-trained embeddings")
    parser.add_argument("--input", "-i", default="data/abstracts.json",
                        help="descriptions file")
    parser.add_argument("--validate", "-v", default="data/abstracts.json",
                        help="abstracts file to validate the output")
    parser.add_argument("--epochs", "-e", default="100",
                        help="set the number of epochs for training")
    parser.add_argument("--size", "-s", default="100",
                        help="set the size of the embeddings")
    parser.add_argument("--hidden_layer", "-o", default="50",
                        help="set the size of the hidden layer")
    parser.add_argument("--seq_len", "-l", default="1",
                        help="set the length of the input sequence")
    parser.add_argument("--num_layers", "-n", default="2",
                        help="set the number of hidden layers in RNN")
    args = parser.parse_args()
    saved_model = args.model
    descriptions_file = args.input
    abstracts_file = args.validate
    model = DescriptionEncoder(int(args.size),
                               int(args.hidden_layer),
                               int(args.seq_len),
                               int(args.num_layers))
    epochs = int(args.epochs)
    x, y, wv = create_mappings(saved_model, descriptions_file)
    train(x, y, wv, model, epochs, abstracts_file)

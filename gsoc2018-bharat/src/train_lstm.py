import torch
import torch.autograd as autograd
import torch.nn as nn
from torch.autograd import Variable
# import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import json
from gensim.models import FastText
import logging
import sys
import matplotlib.pyplot as plt

torch.manual_seed(1)

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO


def load_tensors(directory):
    """
    Input to an LSTM must be a 3D tensor. For that, I
    am reading all the descriptions line by line and
    storing their embeddings row wise into a numpy
    array of 3 dimensions and shape (n, 500, 300).
    """
    logging.info('loading saved embeddings')
    X = np.load(directory + '/description.npy')
    y = np.load(directory + '/entity.npy')
    logging.info('loaded {0} saved embeddings'.format(len(X)))
    train(X, y)


class DescriptionEncoder(nn.Module):
    def __init__(self, hidden_size):
        super(DescriptionEncoder, self).__init__()
        self.hidden_size = hidden_size

        self.inp = nn.Linear(hidden_size, hidden_size)
        # self.lstm = nn.LSTM(hidden_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, 2)
        self.rnn = nn.RNN(hidden_size, hidden_size, 2)
        self.out = nn.Linear(hidden_size, hidden_size)

    def forward(self, inp_desc, hidden=None):
        inp_desc = self.inp(inp_desc)
        # output, hidden = self.rnn(self.lstm(inp_desc)[0])
        output, hidden = self.rnn(self.lstm(inp_desc)[0])
        output = self.out(output)

        return output, hidden


def train(x, y):
    epochs = 500
    hidden_size = 300
    model = DescriptionEncoder(hidden_size)
    inputs = x
    labels = y
    criterion = nn.CosineEmbeddingLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    count = 0
    losses = np.zeros(epochs)
    logging.info('training on {0} samples'.format(len(inputs)))
    for epoch in range(epochs):
        flags = autograd.Variable(torch.ones(1))
        count = 0
        # logging.info('training epoch {0}'.format(epoch + 1))
        for i, l in zip(inputs, labels):
            output, hidden = model(autograd.Variable(torch.tensor([i])), None)
            optimizer.zero_grad()
            # logging.info('{0}'.format(output[0][-1].unsqueeze(1).t().size()))
            loss = criterion(output[0][-1].unsqueeze(1).t(),
                             Variable(torch.tensor([l])),
                             flags)
            loss.backward()
            optimizer.step()
            count + 1
        logging.info(
            'completed epoch {0}, loss : {1}'.format(epoch + 1, loss.item()))
        losses[epoch] = loss.item()
    logging.info('saving the model to model/description_encoder')
    torch.save(model, 'model/description_encoder')
    validate(model)
    plt.plot(losses)
    plt.title('Model Loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.show()


def validate(model):
    m = FastText.load('model/entity_fasttext_n300')
    wv = m.wv
    del m
    shape = (500, 300)

    with open('data/train.json') as input_file:
        for line in input_file:
            json_line = json.loads(line)
            target = [_ for _ in json_line.keys()][0]
            desc = json_line[target].split()
            t = np.zeros(shape, dtype=np.float32)
            # v = np.array(wv.get_vector(ent), dtype=np.float32)
            r = np.array(list(map(lambda x: wv.get_vector(x), desc)),
                         dtype=np.float32)
            t[:r.shape[0], :r.shape[1]] = r
            p = model(autograd.Variable(torch.tensor([t])))[0][0][-1]
            p = p.detach().numpy()
            print('Entity : ' + target)
            print('Predicted : ', end='')
            print(wv.similar_by_vector(p))
            break


if __name__ == '__main__':
    directory = sys.argv[1]
    load_tensors(directory)

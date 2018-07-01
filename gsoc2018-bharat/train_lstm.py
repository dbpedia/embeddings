import torch
import torch.autograd as autograd
import torch.nn as nn
# import torch.nn.functional as F
import torch.optim as optim
import numpy as np
# import json
# from gensim.models import FastText
import logging
import sys

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


class RNNModel(nn.Module):
    def __init__(self, hidden_size):
        super(RNNModel, self).__init__()
        self.hidden_size = hidden_size

        self.inp = nn.Linear(hidden_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, 2, dropout=0.05)
        self.rnn = nn.RNN(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, hidden_size)

    def forward(self, inp_desc, hidden=None):
        inp_desc = self.inp(inp_desc)
        output, hidden = self.rnn(self.lstm(inp_desc)[0])
        output = self.out(output)

        return output, hidden


def train(x, y):
    epochs = 100
    hidden_size = 300
    model = RNNModel(hidden_size)
    # inputs = x[:10]
    # labels = y[:10]
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    count = 0
    # losses = np.zeros(epochs)
    logging.info('train on {0} samples'.format(len(x)))
    for epoch in range(epochs):
        count = 0
        # logging.info('training epoch {0}'.format(epoch + 1))
        for i, l in zip(x[:10], y[:10]):
            output, hidden = model(autograd.Variable(torch.tensor([i])), None)
            optimizer.zero_grad()
            loss = criterion(output[0][-1], autograd.Variable(torch.tensor(l)))
            loss.backward()
            optimizer.step()
            count + 1
        logging.info(
            'completed epoch {0}, loss : {1}'.format(epoch + 1, loss.item()))


if __name__ == '__main__':
    directory = sys.argv[1]
    load_tensors(directory)

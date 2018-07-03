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

from Encoder import DescriptionEncoder

torch.manual_seed(1)

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO


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


def train(x, y):
    epochs = 10
    hidden_size = 100
    model = DescriptionEncoder(hidden_size)
    inputs = x
    labels = y
    itr = len(inputs)
    progress = 0.0
    # criterion = nn.CosineEmbeddingLoss()
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.05)
    count = 0
    itr_p = 0.0
    losses = np.zeros(epochs)
    logging.info('training on {0} samples'.format(itr))
    for epoch in range(epochs):
        logging.info(
            'starting epoch {0}'.format(epoch + 1))
        flags = autograd.Variable(torch.ones(1))
        count = 0
        # logging.info('training epoch {0}'.format(epoch + 1))
        for i, l in zip(inputs, labels):
            # if itr_p % 1.25 == 0:
            #     itr_p += 1.25
            #     logging.info(
            #         'PROGRESS : {0} %'.format(progress))
            print('INFO : PROGRESS : {0:.1f} %'.format(progress), end='\r')
            output, hidden = model(autograd.Variable(torch.tensor([i])), None)
            optimizer.zero_grad()
            # logging.info('{0}'.format(output[0][-1].unsqueeze(1).t().size()))
            loss = criterion(output[0][-1],
                             Variable(torch.tensor(l)))
            # loss = criterion(output[0][-1].unsqueeze(1).t(),
            #                  Variable(torch.tensor([l])),
            #                  flags)
            loss.backward()
            optimizer.step()
            count += 1
            progress = (count / itr) * 100
        logging.info(
            'completed epoch {0}, loss : {1}'.format(epoch + 1, loss.item()))
        losses[epoch] = loss.item()
    logging.info('saving the model to model/description_encoder')
    torch.save(model, 'model/description_encoder')
    validate(model)
    # plt.plot(losses)
    # plt.title('Model Loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.show()


def validate(model):
    m = FastText.load('model/entity_fasttext_n100')
    wv = m.wv
    del m
    shape = (500, 100)

    with open('data/descriptions.json', 'r') as input_file:
        with open('data/validate', 'w+') as output_file:
            for line in input_file:
                json_line = json.loads(line)
                target = [_ for _ in json_line.keys()][0]
                desc = json_line[target].split()
                t = np.zeros(shape, dtype=np.float32)
                # v = np.array(wv.get_vector(ent), dtype=np.float32)
                try:
                    r = np.array(list(map(lambda x: wv.get_vector(x), desc)),
                                 dtype=np.float32)
                except KeyError:
                    continue
                out = len(r)
                t[:r.shape[0], :r.shape[1]] = r
                p = model(autograd.Variable(torch.tensor([t])))[0][0][out]
                p = p.detach().numpy()
                print('Entity : ' + target)
                print('Predicted : ', end='')
                print(wv.similar_by_vector(p))
                output_file.write(target + '\n')
                output_file.write(str(wv.similar_by_vector(p)) + '\n')


if __name__ == '__main__':
    directory = sys.argv[1]
    load_tensors(directory)

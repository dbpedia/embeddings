import torch
import torch.nn as nn
from torch.autograd import Variable


class DescriptionEncoder(nn.Module):
    """
    This class is for the Description Encoder
    which is a stacked LSTM. It can be used to
    encode a given input, a description of an entity,
    and outputs the embedding for that entity.
    """
    def __init__(self, embed_size, hidden_size, seq_len, num_layers):
        """
        Initialize the model

        Arguments
        ---------
        embed_size : Size of the pre-trained embeddings
        hidden_size : Size of the hidden layers
        seq_len : Length of input sequence
        num_layers : Number of layers in the LSTM
        """
        super(DescriptionEncoder, self).__init__()
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.seq_len = seq_len
        self.num_layers = num_layers
        self.inp = nn.Linear(embed_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size // 2, 1,
                            batch_first=True)
        self.rnn = nn.RNN(hidden_size // 2, hidden_size,
                          num_layers, batch_first=True)
        self.out = nn.Linear(hidden_size, embed_size)

    def forward(self, inp_desc, hidden=None):
        if hidden is None:
            hidden = self.init_hidden()
        inp_desc = self.inp(inp_desc)
        output, hidden = self.rnn(self.lstm(inp_desc)[0])
        output = self.out(output)

        return output, hidden

    def init_hidden(self):
        return Variable(torch.zeros(self.num_layers,
                                    self.seq_len,
                                    self.hidden_size))

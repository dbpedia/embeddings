import torch
import torch.nn as nn
from torch.autograd import Variable


class DescriptionEncoder(nn.Module):
    def __init__(self, embed_size, hidden_size, seq_len, num_layers):
        super(DescriptionEncoder, self).__init__()
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.seq_len = seq_len
        self.num_layers = num_layers
        # self.inp = nn.Linear(embed_size, hidden_size)
        # self.gru = nn.GRU(hidden_size, hidden_size, 2)
        self.lstm = nn.LSTM(embed_size, hidden_size, 1,
                            batch_first=True)
        self.rnn = nn.RNN(hidden_size, embed_size,
                          num_layers, batch_first=True)
        # self.out = nn.Linear(hidden_size // 2, embed_size)

    def forward(self, inp_desc, hidden=None):
        if hidden is None:
            hidden = self.init_hidden()
        # inp_desc = self.inp(inp_desc)
        # output, hidden = self.rnn(self.lstm(inp_desc)[0])
        # output, hidden = self.rnn(self.lstm(self.gru(inp_desc)[0])[0])
        # output, hidden = self.lstm(inp_desc)
        output, hidden = self.rnn(self.lstm(inp_desc)[0])
        # output = self.out(output)

        return output, hidden

    def init_hidden(self):
        return Variable(torch.zeros(self.num_layers,
                                    self.seq_len,
                                    self.hidden_size))

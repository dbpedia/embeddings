import torch.nn as nn


class DescriptionEncoder(nn.Module):
    def __init__(self, hidden_size):
        super(DescriptionEncoder, self).__init__()
        self.hidden_size = hidden_size

        self.inp = nn.Linear(hidden_size, hidden_size)
        # self.lstm = nn.LSTM(hidden_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, 2)
        self.lstm = nn.LSTM(hidden_size, hidden_size, 2)
        self.rnn = nn.RNN(hidden_size, hidden_size, 2)
        self.out = nn.Linear(hidden_size, hidden_size)

    def forward(self, inp_desc, hidden=None):
        inp_desc = self.inp(inp_desc)
        # output, hidden = self.rnn(self.lstm(inp_desc)[0])
        output, hidden = self.rnn(self.lstm(self.gru(inp_desc)[0])[0])
        output = self.out(output)

        return output, hidden

from torch import nn
import torch.nn.functional as F

class DQN(nn.Module):

    def __init__(self, num_hidden, input_size, output_size):
        nn.Module.__init__(self)
        self.l1 = nn.Linear(input_size, num_hidden)
        self.l2 = nn.Linear(num_hidden, output_size)

    def forward(self, x):
        return self.l2(F.relu(self.l1(x)))

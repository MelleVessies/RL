from torch import nn
from torch import cuda
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, num_hidden, input_size, output_size, device='cpu'):
        nn.Module.__init__(self)

        self.model = nn.Sequential(
            nn.Linear(input_size, num_hidden),
            nn.ReLU(),
            nn.Linear(num_hidden, num_hidden),
            nn.ReLU(),
            nn.Linear(num_hidden, output_size),
        )

        self.model.to(device)

    def forward(self, x):
        return self.model(x)

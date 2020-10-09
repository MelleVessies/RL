import torch
import numpy as np
class EpsilonGreedyPolicy(object):
    """
    A simple epsilon greedy policy.
    """

    def __init__(self, Q, epsilon, device='cpu'):
        self.Q = Q
        self.epsilon = epsilon
        self.device = device

        self.Q.to(device)

    def sample_action(self, obs):
        """
        This method takes a state as input and returns an action sampled from this policy.

        Args:
            obs: current state

        Returns:
            An action (int).
        """
        x = torch.from_numpy(obs).float().to(self.device)

        with torch.no_grad():
            actions = self.Q(x)

        if np.random.uniform() > self.epsilon:
            return actions.max(0)[1].item()
        else:
            return np.random.randint(actions.size()[0])

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

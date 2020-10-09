from torch import nn
import torch.nn.functional as F

class DQNWrapper():

    def __init__(self, args, input_size, output_si  ze):
        self.Q = DQN(args.num_hidden, input_size, output_size)
        self.memory = ReplayMemory(args.experience_replay_capacity)

        if args.double_q_network:
            self.type = "double DQN"
            self.Q2 = DQN(args.num_hidden, input_size, output_size)
            self.memory2 = ReplayMemory(args.experience_replay_capacity)

        elif args.target_network:
            self.type = "target DQN"
            self.update_iter = args.target_network
            self.target_Q = DQN(args.num_hidden, input_size, output_size)
            self.target_Q.load_state_dict(self.Q.state_dict())
            self.target_Q.eval()

        else:
            self.type = "normal DQN"

    def update_target(self, it):
        if self.type == "target_DQN":
            if it % self.update_iter == 0:
                self.target_Q.load_state_dict(self.Q.state_dict())

    def wrapper_magic(self):
        """ Returns the Q network (+relevant memory) to update and the Q network to evaluate with.
            This is the reason we included the wrapper class at all

            Returns:
            - tuple: (<Q network to update>, <memory for the Q network>, <Q network to evaluate with>)
        """
        if self.type == "double DQN":

            # Choose which network to update at random
            if np.random.random() > 0.5:
                return self.Q, self.memory, self.Q2
            else
                return self.Q2, self.memory2, self.Q

        elif self.type == "target_DQN":
            return self.Q, self.memory, self.target_Q

        elif self.type == "normal DQN":
            return self.Q, self.memory, self.Q

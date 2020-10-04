import random

class ReplayMemory:
    '''Replay memory object in which transitions can be stored for training'''

    def __init__(self, capacity):
        if not isinstance(capacity, int):
            raise ValueError(f"expected integer for capacity of replaybuffer, got {type(capacity)}")
        if capacity < 1:
            raise ValueError(f"expected integer larger than or equal to 1 for capacity of replaybuffer, got {capacity}")
            
        self.capacity = capacity
        self.memory = []

    def push(self, transition):
        if len(self.memory) == self.capacity:
            self.memory = self.memory[1:] + [transition]
        else:
            self.memory.append(transition)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

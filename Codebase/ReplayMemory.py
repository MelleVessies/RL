import random
import numpy as np

class ReplayMemory:
    '''Replay memory object in which transitions can be stored for training'''

    def __init__(self, capacity, flush_memory_after_sample):
        if not isinstance(capacity, int):
            raise ValueError(f"expected integer for capacity of replaybuffer, got {type(capacity)}")
        if capacity < 1:
            raise ValueError(f"expected integer larger than or equal to 1 for capacity of replaybuffer, got {capacity}")

        self.capacity = capacity
        self.flush = flush_memory_after_sample

        self.memory = []

    def push(self, transition):
        if len(self.memory) == self.capacity:
            self.memory = self.memory[1:] + [transition]
        else:
            self.memory.append(transition)

    def sample(self, batch_size):
        s = random.sample(self.memory, batch_size)
        if self.flush:
            self.memory = []
        return s

    def get_all(self):
        return self.memory

    def __len__(self):
        return len(self.memory)

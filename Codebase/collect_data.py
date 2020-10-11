

import warnings
import numpy as np
# from somewhere import run_settings

import json
import argparse
import gym
import numpy as np
import torch
import random
import os
import itertools

from Codebase.DQN import DQN
from Codebase.train import run_episodes, train
from Codebase.ReplayMemory import ReplayMemory
from Codebase.environment import make_env_info
from Codebase.data_handling import DataHandler
from Codebase.Animation import create_animation
from Codebase.DQNWrapper import DQNWrapper

policy_options = ["EpsilonGreedyPolicy"]



def Discrete(x):
    '''Helper function for data loading'''
    return True, int(x)

def Box(*args):
    '''Helper function for data loading'''
    return False, args


def set_seeds(seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)





def add_settings_to_default(base_settings, extra_settings):
    new_setting_dict = {}
    for k,v in base_settings.items():
        new_setting_dict[k] = v
    for k,v in extra_settings.items():
        new_setting_dict[k] = v
    return new_setting_dict

class PseudoArgs:
    def __init__(self, argument_dictionary):
        for k,v in argument_dictionary.items():
            if k == 'policy':
                exec(f"self.{k} = None")
                self.policy = v
            else:
                exec(f"self.{k} = {v}")

    def __str__(self):
        return str(vars(self))



def grid_search(run_settings_func, base_settings, environments, range_epsilon, range_discount, seed_range, skip_completed=True):
    for name in environments:
        make_env_info([eval(name)])
        for epsilon in range_epsilon:
            for discount_factor in range_discount:
                for seed in seed_range:
                    args = PseudoArgs(add_settings_to_default(base_settings, {"environment_name":name,"eps_min":epsilon,"discount_factor":discount_factor, "seed":seed}))
                    print(vars(args))
                    run_settings_func(args, skip_completed=skip_completed)
                # subprocess.call(['./abc.py', arg1, arg2])

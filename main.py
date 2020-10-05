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
from Codebase.EpsilonGreedyPolicy import EpsilonGreedyPolicy
from Codebase.environment import make_env_info

policy_options = ["EpsilonGreedyPolicy"]


def Discrete(x):
    '''Helper function for data loading'''
    return True, int(x)

def Box(*args):
    '''Helper function for data loading'''
    return False, args


def save_data(args, episode_durations, episode_returns, starting_states):
    """saves a json with run results and properties of a run, like
    hyperparameters, environment etc.

    load results with load_data()



    Parameters
    ----------
    args : Namespace
        output of argparse.
    episode_durations : list of ints
        number of steps per epsiode
    episode_returns : list of rewards, depends on environment
        total reward (undiscounted) per episode
    starting_states : list of starting starting_states per episode

    Returns
    -------
    None
    """
    datadict = vars(args)
    fname = ",".join(sorted([k[0] + str(v) for k,v in datadict.items()]))

    datadict["episode_durations"] = episode_durations
    datadict["episode_returns"] = episode_returns
    datadict["starting_states"] = starting_states

    if not os.path.exists("results"):
        os.mkdir("results")


    with open(os.path.join("results", fname), "w+") as f:
        json.dump(datadict, f, indent=4)


def dict_match(filter, dictionary):
    """checks whether all key value pairs in the filter.

    Parameters
    ----------
    filter : dict
        key, value pairs required to be in a dictionary
    dictionary : type
        Description of parameter `dictionary`.

    Returns
    -------
    Bool
        True when all values in the filter occur in the given dictionary
        False when there is any mismatch between the filter and the dictionary
    """
    for k,v in filter.items():
        if not (dictionary[k] == v):
            return False
    return True


def load_data(filter=None):
    """loads in all the result files.

    Returns list of dictionaries with run properties like environment,
    hyperparameters & tricks.

    Using filter returns only those dictionaries where the properties
    correspond to the filter.

    example usage:

    load_data(filter={'environment_name':'Acrobot-v1', 'epsilon':0.05})

    Parameters
    ----------
    filter : dictionary
        properties like in the argparse


    Returns
    -------
    list of dictionaries
        Description of returned object.

    """
    result_files = [f for f in os.listdir("results") if os.path.isfile(os.path.join("results", f))]
    jsons = [json.load(open(os.path.join("results", f), "r")) for f in result_files]

    if not (filter is None):
        filtered_jsons = [result_json for result_json in jsons if dict_match(filter, result_json)]
        return filtered_jsons
    else:
        return jsons


def run_settings(args):
    """collects results for a set of argparse settings.

    Parameters
    ----------
    args : Namespace
        output of argparse.

    Returns
    -------
    None

    """
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)

    env_infodict = json.load(open(os.path.join('environment-info', args.environment_name+".json"), 'r'))

    # make (and SEED) the environment
    env = gym.envs.make(args.environment_name)
    env.seed(args.seed)

    # get variables relevant for the the neural network w.r.t. the environment
    discrete_actions, action_no = eval(env_infodict['action_space'])
    if discrete_actions:
        output_size = action_no

    _, obs_no = eval(env_infodict['observation_space'])
    if len(obs_no) > 1:
        raise ValueError("Convolution still has to be implemented...")
    else:
        input_size = obs_no[0]


    if isinstance(args.clip_grad, float):
        raise ValueError("gradient clipping not yet implemented")

    Q = DQN(args.num_hidden, input_size, output_size)
    memory = ReplayMemory(args.experience_replay_capacity)

    if "EpsilonGreedyPolicy" == args.policy:
        if not isinstance(args.epsilon, float):
            raise ValueError(f"expected float for epsilon, got {args.epsilon}")
        policy = EpsilonGreedyPolicy(Q, args.epsilon)

    episode_durations, episode_returns, starting_states = run_episodes(train, Q, policy, memory, env, args.num_episodes, args.batch_size, args.discount_factor, args.stepsize)
    save_data(args, episode_durations, episode_returns, starting_states)




if __name__ == '__main__':

    envs = ["Acrobot-v1", "CartPole-v1", "MountainCar-v0", "MountainCarContinuous-v0", "Breakout-v0", "MontezumaRevenge-v0"]
    make_env_info(envs)

    parser = argparse.ArgumentParser()
    # env settings
    parser.add_argument('--environment_name', default='CartPole-v1', type=str, help='name of the environment according to the name listed @ https://gym.openai.com/envs/#atari')
    parser.add_argument('--num_episodes', default=200)

    # tricks
    parser.add_argument('--experience_replay_capacity', type=int, default=10000, help="size of the replay buffer, size of 1 implies only the last action is in it, which entails there is no experience rayepl")
    parser.add_argument('--discount_factor', type=float, default=1.02, help='degree to which the future is certain, discount_factor=1 corresponds to certainty about future reward')

    # entwork (training )settings
    parser.add_argument('--clip_grad', type=float, help='gradient clipped to size float, if < 0 (-1) there is no clipping')
    parser.add_argument('--batch_size', type=int, default=64, help='number of state action pairs used per update')
    parser.add_argument('--stepsize', type=float, default=1e-3, help='learning rate')
    parser.add_argument('--num_hidden', type=int, default=256, help='number of hidden units per hidden layer iof the network')

    # policy arguments
    parser.add_argument('--policy', type=str, default="EpsilonGreedyPolicy", help='choice betweem ["EpsilonGreedyPolicy"]')
    parser.add_argument('--epsilon', type=float, default=0.05, help='epsilon (chance to explore) for policies that require it')

    # seed
    parser.add_argument('--seed', type=int, default=42, help="random seed")

    # finish adding arguments
    args = parser.parse_args()

    run_settings(args)
    All_data = load_data()
    Acrobot_data = load_data(filter={"environment_name":"Acrobot-v1"})
    MountainCar_data = load_data(filter={"environment_name":"MountainCar-v0"})

    print(f"got {len(Acrobot_data)} run results for Acrobot")
    print(f"got {len(MountainCar_data)} run results for MountainCar_data")
    print(f"got {len(All_data)} run results for All_data")

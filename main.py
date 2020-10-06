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
from Codebase.data_handling import DataHandler
from Codebase.Animation import create_animation

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


def run_settings(args, datahandler):
    """collects results for a set of argparse settings.

    Parameters
    ----------
    args : Namespace
        output of argparse.

    Returns
    -------
    None

    """
    set_seeds(args.seed)

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

    if args.pretrained:
        Q = datahandler.load_model()
    else:
        Q = DQN(args.num_hidden, input_size, output_size)
    memory = ReplayMemory(args.experience_replay_capacity)

    if "EpsilonGreedyPolicy" == args.policy:
        if not isinstance(args.epsilon, float):
            raise ValueError(f"expected float for epsilon, got {args.epsilon}")
        policy = EpsilonGreedyPolicy(Q, args.epsilon)


    if args.num_episodes > 0:
        episode_durations, episode_returns, starting_states = run_episodes(
            train, Q, policy, memory, env, args.num_episodes, args.batch_size, args.discount_factor, args.stepsize, args.do_train)
        datahandler.save_data(episode_durations, episode_returns, starting_states, Q)

    if args.create_animation:
        create_animation(env, policy)


if __name__ == '__main__':

    envs = ["Acrobot-v1", "CartPole-v1", "MountainCar-v0", "MountainCarContinuous-v0", "Breakout-v0", "MontezumaRevenge-v0"]
    make_env_info(envs)

    parser = argparse.ArgumentParser()
    # env settings
    parser.add_argument('--environment_name', default='CartPole-v1', type=str, help='name of the environment according to the name listed @ https://gym.openai.com/envs/#atari')
    parser.add_argument('--num_episodes', default=200)

    # tricks
    parser.add_argument('--experience_replay_capacity', type=int, default=10000, help="size of the replay buffer, size of 1 implies only the last action is in it, which entails there is no experience rayepl")
    parser.add_argument('--discount_factor', type=float, default=0.8, help='degree to which the future is certain, discount_factor=1 corresponds to certainty about future reward')

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

    # framework settings
    parser.add_argument('--save_network', type=bool, default=False, help='Save the used Q network')
    parser.add_argument('--pretrained', type=bool, default=False, help='Load a pretrained Q network')
    parser.add_argument('--do_train', type=bool, default=True, help='Update the Q network weights while running episodes')
    parser.add_argument('--create_animation', type=bool, default=True, help='Create and save an animation of a single episode')

    # finish adding arguments
    args = parser.parse_args()
    datahandler = DataHandler(args)
    run_settings(args, datahandler)
    All_data = datahandler.load_data()

    Acrobot_data = datahandler.load_data(filter={"environment_name":"Acrobot-v1"})
    MountainCar_data = datahandler.load_data(filter={"environment_name":"MountainCar-v0"})

    print(f"got {len(Acrobot_data)} run results for Acrobot")
    print(f"got {len(MountainCar_data)} run results for MountainCar_data")
    print(f"got {len(All_data)} run results for All_data")

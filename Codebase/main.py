import json
import argparse
import gym

from DQN import DQN
from train import run_episodes, train
from ReplayMemory import ReplayMemory
from EpsilonGreedyPolicy import EpsilonGreedyPolicy

policy_options = ["EpsilonGreedyPolicy"]


def Discrete(x):
    '''Helper function for data loading'''
    return True, int(x)

def Box(*args):
    '''Helper function for data loading'''
    return False, args


def setup(args):
    env_infodict = json.load(open('environment-info.json', 'r'))

    # make the environment
    env = gym.envs.make(args.environment_name)

    # get variables relevant for the the neural network w.r.t. the environment
    discrete_actions, action_no = eval(env_infodict[args.environment_name]['action_space'])
    if discrete_actions:
        output_size = action_no

    _, obs_no = eval(env_infodict[args.environment_name]['observation_space'])
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

    run_episodes(train, Q, policy, memory, env, args.num_episodes, args.batch_size, args.discount_factor, args.stepsize)





if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    # env settings
    parser.add_argument('--environment_name', default='Acrobot-v1', type=str, help='name of the environment according to the name listed @ https://gym.openai.com/envs/#atari')
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
    args = parser.parse_args()

    setup(args)

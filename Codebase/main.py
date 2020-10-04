import json
import argparse
import gym

from DQN import DQN
from train import run_episodes, train
from ReplayMemory import ReplayMemory
from EpsilonGreedyPolicy import EpsilonGreedyPolicy

policy_options = ["EpsilonGreedyPolicy"]


def setup(args):
    env_infodict = json.load(open('environment-info.json', 'r'))
    env_infodict = env_infodict[args.environment_name]
    env = gym.envs.make(args.environment_name)
    for k,v in env_infodict.items():
        print(k, v)


    Q = DQN()
    memory = ReplayMemory(args.experience_replay_capacity)


    policy_class = {"EpsilonGreedyPolicy":EpsilonGreedyPolicy}[args.policy]
    if "Epsilon" in args.policy:
        policy = policy_class(Q, args.epsilon)

    run_episodes(train, Q, policy, memory, env, args.num_episodes, args.batch_size, args.discount_factor, args.stepsize)





if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    # env name
    parser.add_argument('--environment_name', default='CartPole-v1', type=str, help='name of the environment according to the name listed @ https://gym.openai.com/envs/#atari')

    # tricks
    parser.add_argument('--experience_replay_capacity', type=int, help="size of the replay buffer, size of 1 implies only the last action is in it, which entails there is no experience rayepl")
    parser.add_argument('--clip-grad', type=float, help='gradient clipped to size float, if < 0 (-1) there is no clipping')
    parser.add_argument('--batch_size', type=int, help='number of state action pairs used per update')
    parser.add_argument('--discount_factor', type=float, help='degree to which the future is certain, discount_factor=1 corresponds to certainty about future reward')
    parser.add_argument('--stepsize', type=float, help='learning rate')
    parser.add_argument('--num_episodes')
    parser.add_argument('--policy', type=str, help='choice betweem ["EpsilonGreedyPolicy"]')
    parser.add_argument('--epsilon', type=float, help='epsilon (chance to explore) for policies that require it')
    args = parser.parse_args()


    setup(args)

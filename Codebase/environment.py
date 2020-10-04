

import gym
import os
import numpy as np
import json


def make_env_info(environments):
    env_info = {}
    with open("environment-info.json", 'w+') as f:
        for env_name in envs:
            env_info[env_name] = {}
            env = gym.envs.make(env_name)
            sample_output = env.reset()
            env_info[env_name]['shape'] = str(sample_output.shape)
            env_info[env_name]['dtype'] = str(sample_output.dtype)
            env_info[env_name]['action_space'] = str(env.action_space)
            try:
                env_info[env_name]['action_space.high'] = str(env.action_space.high)
                env_info[env_name]['action_space.low'] = str(env.action_space.low)
            except:
                pass
            env_info[env_name]['observation_space'] = str(env.observation_space)
            try:
                env_info[env_name]['observation_space.high'] = str(env.observation_space.high)
                env_info[env_name]['observation_space.low'] = str(env.observation_space.low)
            except:
                pass
            env_info[env_name]['environment web page'] = f"https://gym.openai.com/envs/{env_name}/"
        json.dump(env_info, f, indent=4)




if __name__ == '__main__':
    envs = ["Acrobot-v1", "CartPole-v1", "MountainCar-v0", "MountainCarContinuous-v0", "Breakout-v0", "MontezumaRevenge-v0"]
    make_env_info(envs)

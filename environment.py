

import gym
import os
import numpy as np
import json


envs = ["Acrobot-v1", "CartPole-v1", "MountainCar-v0", "MountainCarContinuous-v0", "Breakout-v0", "MontezumaRevenge-v0"]




if __name__ == '__main__':
    env_info = {}
    with open("environment-info.json", 'w+') as f:
        for env_name in envs:
            env_info[env_name] = {}
            env = gym.envs.make(env_name)
            sample_output = env.reset()
            env_info[env_name]['shape'] = str(sample_output.shape)
            env_info[env_name]['dtype'] = str(sample_output.dtype)
        json.dump(env_info, f, indent=4)

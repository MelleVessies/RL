

import gym
import os
import numpy as np
import json


def make_env_info(environments):
    """records information about a set of environments, which is usefull for
    setting up things like network size.

    OVERWRITES RATHER THAN ADDS
    saves to environment-info/ENVIRONMENT_NAME.json

    result is used in main.py/run_settings

    example usage:
    make_env_info(["Acrobot-v1", "CartPole-v1", "MountainCar-v0"])

    Parameters
    ----------
    environments : list of strings
        explicit names of the environments like they are claled when loading gym.

    Returns
    -------
    None

    """
    if not os.path.exists("environment-info"):
        os.mkdir("environment-info")
    for env_name in environments:
        env_info = {}
        with open(os.path.join("environment-info", f"{env_name}.json"), 'w+') as f:
            env = gym.envs.make(env_name)
            sample_output = env.reset()
            env_info['shape'] = str(sample_output.shape)
            env_info['dtype'] = str(sample_output.dtype)
            env_info['action_space'] = str(env.action_space)
            try:
                env_info['action_space.high'] = str(env.action_space.high)
                env_info['action_space.low'] = str(env.action_space.low)
            except:
                pass
            env_info['observation_space'] = str(env.observation_space)
            try:
                env_info['observation_space.high'] = str(env.observation_space.high)
                env_info['observation_space.low'] = str(env.observation_space.low)
            except:
                pass
            env_info['environment web page'] = f"https://gym.openai.com/envs/{env_name}/"
            json.dump(env_info, f, indent=4)




if __name__ == '__main__':
    envs = ["Acrobot-v1", "CartPole-v1", "MountainCar-v0", "MountainCarContinuous-v0", "Breakout-v0", "MontezumaRevenge-v0"]
    make_env_info(envs)

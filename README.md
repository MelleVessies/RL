# RL

## mediums:
* [git](https://github.com/MelleVessies/RL)
* [environments](https://gym.openai.com/envs/#classic_control)
* [Overleaf](https://www.overleaf.com/5619338925gmhsmbkfvhgw)

## Guide to installing the atari environments

If you're feeling lucky: `pip install gym[atari]` inside the rl2020 environment, otherwise follow (with the rl2020 environment activated):

First install pip for conda:

`conda install pip`

then find out where your environment is located using:

`conda env list`

such that you can install the gym environment with the atari component:

`mypath/to/environment/bin/pip install 'gym[atari]'`

you should now be able to run 'environment.py' to get a rundown of environment properties output in environment-info.json

`python environment.py`

specific properties can be read up on [here](https://gym.openai.com/docs/)
other invironment properties such as max steps & reward treshold for 'solving' an environment are given in the [registry file](https://github.com/openai/gym/blob/master/gym/envs/__init__.py)

## Todo


#### setting up environments :
- [x] [Acrobot (what is its difficulty?)](https://gym.openai.com/envs/Acrobot-v1/)
- [x] [cartpole (what is its difficulty?)](https://gym.openai.com/envs/CartPole-v1/)
- [x] [mountain car (what is its difficulty?)](https://gym.openai.com/envs/MountainCar-v0)
- [ ] [mountain car continuous (what is its difficulty?)](https://gym.openai.com/envs/MountainCar-v0/)
- [ ] [Breakout (what is its difficulty?)](https://gym.openai.com/envs/Breakout-v0/)
- [ ] [Monte Zumas revenge (notoriously difficult)](https://gym.openai.com/envs/MontezumaRevenge-v0/)
- [ ] [other environments...](https://gym.openai.com/envs/#atari)

#### policies
- [x] EpsilonGreedy
- [ ] EpsilongreedyContinuous(?)
- [ ] other?

#### Implementing tricks:
- [x] [experience replay](http://www.incompleteideas.net/lin-92.pdf)  (copied from assignment)
- [ ] [target network](https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf), [target network]((https://arxiv.org/pdf/1708.04133.pdf) (general RL, not necessarily DQN)
- [ ] gradient clipping [see](https://abhishm.github.io/DQN/) [specific, paper source? many papers in use it when searching on scholar but there doesnt seem to be a justifying paper]
- [x] [batch sizes](https://arxiv.org/pdf/1708.04133.pdf) (general RL, not necessarily DQN) (copied from assignment)
- [x] [step size](https://arxiv.org/pdf/1708.04133.pdf) (general RL, not necessarily DQN) (copied from assignment)
- [ ] find more tricks [with source]


#### Algorithm/DQN-related
- [ ] check if we're using the semi-gradient version in the assignment
- [x] hyperparameter parser/config [Codebase/main.py](https://github.com/MelleVessies/RL/blob/main/Codebase/main.py)
- [ ] save results (per environment per hyperparameter settings collect return per epsiode and steps in episode)
- [ ] result graphing

## Ask TA:
* what does a 10 look like for a blog? - could some example of a '9.5+' grade blog be posted blogs?
* Does it have any added value to also look at performance on continuous action spaces?
* For MontezumaRevenge and Breakout, we have the screen as observation, thus we would need to use convolutions. Would this not make it incomparable to the DQN without convolutions for e.g the MountainCar problem?
* should we change early termination criteria so its the same for all environments?


#### Papers
* [DQN-paper/target network/ Human-Level Control
through Deep Reinforcement Learning.](https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf)
* [a brief survey of Deep reinforcement learning](https://arxiv.org/pdf/1708.05866.pdf)
* [experience replay](http://www.incompleteideas.net/lin-92.pdf)
* [OpenAI-gym](https://arxiv.org/pdf/1606.01540.pdf)
* [Deep Reinforcement Learning that Matters](https://arxiv.org/pdf/1709.06560.pdf) #reproducibility
* [Reproducibility of benchmarked deep reinforcement learning tasks for continuous control](https://arxiv.org/pdf/1708.04133.pdf) # hyperparameters matter

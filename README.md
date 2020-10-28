# RL

# SET-UP instructions and requirements:

 python 3.7 was used, to set up the environment run:

 `conda env create -f environment.yml`

In order to open the web page (on linux), run:
`./start_app.sh`

In order to open the web page (on windows), run:

`start_app.sh`

then, open a browser (ideally chrome on full-screen) and manually put "127.0.0.1:5000" in your browser's adress bar.


# Not interesting, legacy:

## mediums:
* [git](https://github.com/MelleVessies/RL)
* [environments](https://gym.openai.com/envs/#classic_control)
* [Overleaf](https://www.overleaf.com/5619338925gmhsmbkfvhgw)
* [blog outline](https://docs.google.com/document/d/1hIE23JBw8bsPUqPMtLHgawx1U3kX7SI54P924oBWXGU/edit)


# Todo


#### setting up environments :
- [x] [Acrobot (what is its difficulty?)](https://gym.openai.com/envs/Acrobot-v1/)
- [x] [cartpole (what is its difficulty?)](https://gym.openai.com/envs/CartPole-v1/)
- [x] [mountain car (what is its difficulty?)](https://gym.openai.com/envs/MountainCar-v0)
- [x] [Lunar lander (what is its difficulty?)](https://gym.openai.com/envs/LunarLander-v2)
- [-] [mountain car continuous (what is its difficulty?)](https://gym.openai.com/envs/MountainCar-v0/) **David says: continuous action spaces are likely out of scope**
- [-] [Breakout (what is its difficulty?)](https://gym.openai.com/envs/Breakout-v0/) **David says: atari environments are likely out of scope**
- [-] [Monte Zumas revenge (notoriously difficult)](https://gym.openai.com/envs/MontezumaRevenge-v0/) **David says: atari environments are likely out of scope**
- [-] [other environments...](https://gym.openai.com/envs/#atari)

#### policies
- [x] EpsilonGreedy
    - [ ] unchanging epsilon
    - [x] decaying epsilon (homework see run_settings and get_epsilon in [train.py](https://github.com/MelleVessies/RL/blob/main/Codebase/train.py))
- [ ] **explicitly not** implemented EpsilonGreedy for **continuous** action spaces, David says its out of scope
- [ ] other?

#### Implementing tricks:
- [x] [experience replay](http://www.incompleteideas.net/lin-92.pdf)  (copied from assignment)
- [x] [target network](https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf), [target network](https://arxiv.org/pdf/1708.04133.pdf) (general RL, not necessarily DQN)
- [x] gradient clipping [see](https://abhishm.github.io/DQN/) [specific, paper source? many papers in use it when searching on scholar but there doesnt seem to be a justifying paper]
- [x] [batch sizes](https://arxiv.org/pdf/1708.04133.pdf) (general RL, not necessarily DQN) (copied from assignment)
- [x] [step size](https://arxiv.org/pdf/1708.04133.pdf) (general RL, not necessarily DQN) (copied from assignment)
- [x] [Double DQN](https://arxiv.org/pdf/1509.06461.pdf)  
- [ ] find more tricks [with source]
- [ ] check slides for lecture mentioned tricks


#### Algorithm/DQN-related
- [x] check if we're using the semi-gradient version in the assignment
- [x] implement choice of full/semi-gradient
- [x] hyperparameter parser/config [Codebase/main.py](https://github.com/MelleVessies/RL/blob/main/main.py)
- [x] save results )
    * saved is json format, see see main.py/load_data, main.py/save_data
    * for each epsiode saves
        * return
        * total steps/episode
        * starting state (nested list format to comply with json)
- [ ] result graphing

## Ask TA (mention DQN):
* Q: what does a 10 look like for a blog? - could some example of a '9.5+' grade blog be posted blogs?
    - A: David will see if he can get some reference blogs to be posted
* Q: Does it have any added value to also look at performance on continuous action spaces?
    - A: likely out of scope
* Q: For MontezumaRevenge and Breakout, we have the screen as observation, thus we would need to use convolutions. Would this not make it incomparable to the DQN without convolutions for e.g the MountainCar problem?
    - A: atari is likely out of scope
* Q: should we change early termination criteria so its the same for all environments?\
    - A: if we can justify it
* Q: currently got acrobot, cartpole, mountaincar.
    - A: three is nice, if anything else make it simple.

* Q: Should we implement any additional tricks learned in the second half of the course?



### other Todo
- [ ] Find out if theres a particular reason some environments have a shorted default termination number of steps than others.
- [ ] Implement a check/warning to see if settings have already been run
- [x] implement a check to see whether all results use the same set of hyperparameters and or filter out incomplete ones
- [x] implement saving NNs to view result

#### useful Papers
* [DQN-paper/target network/ Human-Level Control
through Deep Reinforcement Learning.](https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf)
* [a brief survey of Deep reinforcement learning](https://arxiv.org/pdf/1708.05866.pdf)
* [experience replay](http://www.incompleteideas.net/lin-92.pdf)
* [OpenAI-gym](https://arxiv.org/pdf/1606.01540.pdf)
* [Deep Reinforcement Learning that Matters](https://arxiv.org/pdf/1709.06560.pdf) #reproducibility
* [Reproducibility of benchmarked deep reinforcement learning tasks for continuous control](https://arxiv.org/pdf/1708.04133.pdf) # hyperparameters matter
* [What Matters In On-Policy Reinforcement Learning?](https://arxiv.org/pdf/2006.05990.pdf) #tricks for on-policy learning in continuous environments might have some useful tricks

## Install box2d environment

see https://medium.com/@sayanmndl21/install-openai-gym-with-box2d-and-mujoco-in-windows-10-e25ee9b5c1d5

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


# d3: pages
- [heatmap](https://www.d3-graph-gallery.com/graph/heatmap_tooltip.html)
- [line chart](https://www.d3-graph-gallery.com/graph/line_confidence_interval.html)
- [greek letters](http://www.javascripter.net/faq/greekletters.htm)

##Latest TODOS
- [x] Create wrapper class around Q network
- [x]  Wrapper class should allow target network implementation
- [x]  Wrapper class should allow double Q learning implementation
- [x]  Fix gradient clipping
- [ ] Add some more styling/structure to the website
- [x] Make it possible to disable replay memory (implemented, simply set argument 'experience_replay_capacity' to 0)
- [ ] Set up a function that makes it easier to run a bunch of different settings in sequence and gather results
- [ ] Create function that creates plots for gathered data
        - [ ] graph average returns, number of steps, over seeds per parameter with stdev
        - [ ] grid-search like fashion for basic values for epsilon & discount
- [ ] add section to blog talking about reward
- [ ] option to create multiple sample videos
- [ ] make load_data static


## Hyperparameter searches
- 10 seeds?

- No tricks
- ReplayMemory
- Target network
- All tricks

- IF TIME:

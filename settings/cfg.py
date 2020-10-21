no_tricks_settings = {
    "num_episodes": 200,
    "max_episode_steps":0,

    # Experiment ding
    "experience_replay_capacity":0,
    # "experience_replay_capacity":10000,

    "clip_grad":-1,
    "batch_size":64,
    "stepsize": 1e-3,
    "num_hidden":128,
    "full_gradient":False,
    "policy":"EpsilonGreedyPolicy",
    "eps_steps_till_min":10,
    "save_network":True,
    "pretrained":False,
    "double_q_network": False,

    # Experiment ding
    "target_network":False,
    # "target_network":True,

    "do_not_train":False,
    "create_animation":False,
    "skip_run_episodes":False
}

grid_search_range = {
    "eps_min":[0.05*i for i in range(1, 8)],
    "discount_factor": [round(0.7 + 0.05*i, 2) for i in range(7)]
}

training_seed_range = [i for i in range(1, 6)]
eval_seed_range = [i for i in range(6, 11)]

print("training_seed_range", training_seed_range)
print("eval_seed_range", eval_seed_range)
print(grid_search_range['eps_min'])
print(grid_search_range['discount_factor'])

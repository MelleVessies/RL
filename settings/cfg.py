no_tricks_settings = {
    "num_episodes": 200,
    "max_episode_steps":0,
    "experience_replay_capacity":0,
    "clip_grad":-1,
    "batch_size":64,
    "stepsize": 1e-3,
    "num_hidden":128,
    "full_gradient":False,
    "policy":"EpsilonGreedyPolicy",
    "eps_steps_till_min":1,
    "save_network":False,
    "pretrained":False,
    "double_q_network": False,
    "target_network":False,
    "do_not_train":False,
    "create_animation":False,
    "skip_run_episodes":False
}

grid_search_range = {
    "eps_min":[.1*i for i in range(11)],
    "discount_factor": [round(.8+ 0.02*i, 2) for i in range(11)]
}

training_seed_range = [i for i in range(10)]
eval_seed_range = [i for i in range(10,20)]

print("training_seed_range", training_seed_range)
print("eval_seed_range", eval_seed_range)
print(grid_search_range['eps_min'])
print(grid_search_range['discount_factor'])

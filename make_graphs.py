import numpy as np
import os
from collections import defaultdict

from Codebase.data_handling import DataHandler
from Codebase.collect_data import add_settings_to_default
import settings.cfg as cfg


def plot_gridsearch_dummy(file):
    pass




def get_num_steps_final(json):
    return json['episode_durations'][-1]

def get_value_return_final(json):
    return json['episode_returns'][-1]


def training_seed_result_gridsearch(base_settings, seed_range, grid_value, environment):
    filter = add_settings_to_default(eval(f"cfg.{base_settings}"), {"environment_name":environment})
    jsons = DataHandler.load_data(filter=filter)

    if grid_value == 'return':
        variabe_lambda = get_value_return_final
    if grid_value == 'steps':
        variabe_lambda = get_num_steps_final
    combination = defaultdict(list)
    for data in jsons:
        if data['seed'] in seed_range:
            combination[(data["eps_min"], data['discount_factor'])].append(variabe_lambda(data))


    filename_base = os.path.join(os.path.join("app", "static"), "csv")
    graph_name = f"grid-{base_settings}-{environment}-{grid_value}.csv"

    with open(os.path.join(filename_base, graph_name), "w+") as f:
        f.write("Epsilon,Discount,value\n")
        for k,v in combination.items():
            f.write(f"{round(k[0], 2)},{k[1]},{np.mean(v)}\n")




training_seed_result_gridsearch("no_tricks_settings", cfg.training_seed_range, "return", "CartPole-v1")

jsons = DataHandler.load_data(filter={"eps_min":0.9})
print(len(jsons))

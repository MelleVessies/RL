from flask import Flask,render_template, request
import numpy as np
import json
from . import main
import os
from collections import defaultdict


@main.route('/', methods=['GET'])
def index():
    return render_template("base.html")

# Example of loading a page by url, preferable through ajax in js
@main.route('/example', methods=['GET'])
def example():
    return render_template("base.html")

@main.route("/getPage", methods=['GET'])
def renderPage():
    type = request.args.get('type')
    if type not in ['home', 'credits', 'blog']:
        print("invalid page")

    return render_template(type + ".html")

@main.route('/run_ajax', methods=['GET'])
def getEpisode():
    # data wil contain eps, discount, etc
    data = json.loads(request.args.get('data'))

    # return video url
    return json.dumps(["/static/videos/animation_2.mp4"])

def group_results():
    all_results_dir = 'results'
    envdirs = os.listdir(all_results_dir)

    result_list = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for env_res_dir in [os.path.join(all_results_dir, envdir) for envdir in envdirs]:
        env_results = os.listdir(env_res_dir)
        for res_dir in [os.path.join(env_res_dir, env_result) for env_result in env_results]:
            res_json_file = os.path.join(res_dir, 'results.json')

            with open(res_json_file) as f:
                res = json.load(f)
                res['req_path'] = "/static/" + res_json_file
                # res['avg_final_performance'] = sum(res['MSTD_errors']) / len(res['MSTD_errors'])

            try:
                res.pop('MSTD_errors')
                res.pop('starting_states')
                res.pop('episode_durations')
                res.pop('episode_returns')
            except:
                print(f'WARNING: seems like {res_json_file} is incomplete')
                continue

            tricks_key = 'Replay_' + str(res['experience_replay_capacity']) + '__Target_' + str(res['target_network'])

            result_list[res['environment_name']][tricks_key][res['seed']].append(res)

    return result_list

def create_avg_over_seeds(result_list):
    for env, env_results in result_list.items():
        for tricks_key, trick_results in env_results.items():
            heatmap_running = defaultdict(lambda: defaultdict(list))
            heatmap_data = []

            for seed, seed_res in trick_results.items():
                for run_res in seed_res:
                    heatmap_running[run_res['eps_min']][run_res['discount_factor']].append(run_res['avg_final_performance'])

            for epsilon, discount_factors in heatmap_running.items():
                for discount_factor, values in discount_factors.items():
                    heatmap_data.append({
                        'discount_factor': round(discount_factor, 2),
                        'epsilon': round(epsilon, 2),
                        'value': round(sum(values)/len(values), 2)
                    })

            result_list[env][tricks_key]['grid_search'] = heatmap_data
    return result_list



@main.route("/list_results", methods=['GET'])
def getResultList():
    result_list = create_avg_over_seeds(group_results())

    return json.dumps(result_list)
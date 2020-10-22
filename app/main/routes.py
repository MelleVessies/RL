from flask import Flask,render_template, request
import numpy as np
import json
from . import main
import os
from collections import defaultdict
import time


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

                r = res['MSTD_errors']
                MSTDS = np.array(r[1:])
                MSTDS_ = np.array(r[:-1])
                avg_growth = np.mean(MSTDS/MSTDS_)

                res['avg_growth'] = avg_growth

            try:
                res.pop('MSTD_errors')
                res.pop('starting_states')
                res.pop('episode_durations')
                #res.pop('episode_returns')
                res.pop('skip_run_episodes')
                res.pop('stepsize')
                res.pop('final_performance')
            except:
                print(f'WARNING: seems like {res_json_file} is incomplete')
                continue

            tricks_key = 'Replay_' + str(res['experience_replay_capacity']) + '__Target_' + str(res['target_network'])

            result_list[res['environment_name']][tricks_key][res['seed']].append(res)

    return result_list

def create_avg_over_seeds(result_list):
    print("\n Now creating seed avgs \n")
    for env, env_results in result_list.items():
        trick_returns = defaultdict(dict)

        for tricks_key, trick_results in env_results.items():
            print(f"Now running for {env} + {tricks_key} \n")
            MSTD_errors = []
            returns = defaultdict(dict)
            returns_for_avg = []

            heatmap_running = defaultdict(lambda: defaultdict(list))
            heatmap_data = []

            for seed, seed_res in trick_results.items():
                for run_res in seed_res:
                    heatmap_running[run_res['eps_min']][run_res['discount_factor']].append([
                        run_res['avg_final_performance'],
                        run_res['avg_growth']
                    ])
                    # TODO this means we are taking the final hyper parameter combination of the seed. this should be the best!!!
                    returns[seed] = [{'x': x, 'y': y} for x, y in enumerate(run_res['episode_returns'])]
                    # TODO here we are appending all episode returns, which should also be the best only
                    returns_for_avg.append(run_res['episode_returns'])

            # TODO, yea, if this breaks we have inconsistent numbers of episodes
            returns_for_avg = np.mean(np.array(returns_for_avg), axis=0)
            trick_returns[tricks_key] = [{'x': x, 'y': y} for x, y in enumerate(list(returns_for_avg))]

            for epsilon, discount_factors in heatmap_running.items():
                for discount_factor, values in discount_factors.items():
                    values = np.array(values)

                    heatmap_data.append({
                        'discount_factor': round(discount_factor, 2),
                        'epsilon': round(epsilon, 2),
                        'return': round(sum(values[:, 0])/len(values[:, 0]), 2),
                        'growth': round(sum(values[:, 1])/len(values[:, 1]), 2)
                    })

            # result_list[env][tricks_key]['MSTD_errors'] = MSTD_errors
            result_list[env][tricks_key] = {
                'returns':  returns,
                'grid_search': heatmap_data
            }

        result_list[env]["all_tricks"] = {
            'returns': trick_returns,
        }

    return result_list



@main.route("/list_results", methods=['GET'])
def getResultList():
    result_list = create_avg_over_seeds(group_results())
    return json.dumps(result_list)

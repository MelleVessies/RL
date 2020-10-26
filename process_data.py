import numpy as np
import json
import os
from collections import defaultdict

def group_results():
    all_results_dir = 'results'
    envdirs = os.listdir(all_results_dir)

    result_list = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for env_res_dir in [os.path.join(all_results_dir, envdir) for envdir in envdirs if os.path.isdir(os.path.join(all_results_dir, envdir))]:
        env_results = os.listdir(env_res_dir)
        for res_dir in [os.path.join(env_res_dir, env_result) for env_result in env_results]:
            res_json_file = os.path.join(res_dir, 'results.json')

            with open(res_json_file) as f:
                res = json.load(f)
                res['req_path'] = "/static/" + res_json_file

                # r = res['MSTD_errors']
                # MSTDS = np.array(r[1:])
                # MSTDS_ = np.array(r[:-1])
                # avg_growth = np.mean(MSTDS/MSTDS_)
                #
                # res['avg_growth'] = avg_growth

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
        trick_returns_std = defaultdict(dict)

        upper, lower = None, None

        for tricks_key, trick_results in env_results.items():
            print(f"Now running for {env} + {tricks_key} \n")
            MSTD_errors = []
            returns = defaultdict(dict)
            returns_std = defaultdict(dict)
            returns_for_avg = []

            heatmap_running = defaultdict(lambda: defaultdict(list))
            heatmap_data = []

            for seed, seed_res in trick_results.items():
                for run_res in seed_res:

                    if upper is not None:
                        if upper < run_res['avg_final_performance']:
                            upper = run_res['avg_final_performance']
                    else:
                        upper = run_res['avg_final_performance']

                    if lower is not None:
                        if lower > run_res['avg_final_performance']:
                            lower = run_res['avg_final_performance']
                    else:
                        upper = run_res['avg_final_performance']

                    heatmap_running[run_res['eps_min']][run_res['discount_factor']].append([
                        run_res['avg_final_performance'],
                        # run_res['avg_growth']
                    ])
                    # TODO this means we are taking the final hyper parameter combination of the seed. this should be the best!!!
                    returns[seed] = [{'x': x, 'y': y} for x, y in enumerate(run_res['episode_returns'])]
                    # TODO here we are appending all episode returns, which should also be the best only
                    returns_for_avg.append(run_res['episode_returns'])

            # TODO, yea, if this breaks we have inconsistent numbers of episodes
            returns_std_for_avg = np.std(np.array(returns_for_avg), axis=0)
            returns_for_avg = np.mean(np.array(returns_for_avg), axis=0)


            trick_returns[tricks_key] = [{'x': x, 'y': y} for x, y in enumerate(list(returns_for_avg))]
            trick_returns_std[tricks_key] = [{'x': x, 'y': y} for x, y in enumerate(list(returns_std_for_avg))]

            for epsilon, discount_factors in heatmap_running.items():
                for discount_factor, values in discount_factors.items():
                    values = np.array(values)

                    heatmap_data.append({
                        'discount_factor': round(discount_factor, 2),
                        'epsilon': round(epsilon, 2),
                        'return': round(sum(values[:, 0])/len(values[:, 0]), 2),
                        # 'growth': round(sum(values[:, 1])/len(values[:, 1]), 2)
                    })

            # result_list[env][tricks_key]['MSTD_errors'] = MSTD_errors
            result_list[env][tricks_key] = {
                'returns': returns,
                'grid_search': heatmap_data
            }
        result_list[env]['heatmap_bounds'] = {'upper': upper, 'lower': lower}
        result_list[env]["all_tricks"] = {
            'returns': trick_returns,
            'returns_std': trick_returns_std #figure out how to get std :(
        }

    return result_list

if __name__ == '__main__':
    results = create_avg_over_seeds(group_results())
    with open('results/processed_data.json', 'w') as f:
        json.dump(results, f)

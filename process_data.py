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

                r = res['MSTD_errors']
                # MSTDS = np.array(r[1:])
                # MSTDS_ = np.array(r[:-1])
                MSTDS = np.array(r[-1])
                MSTDS_ = np.array(r[0])
                avg_growth = np.mean(np.log10(MSTDS/MSTDS_))

                res['avg_growth'] = avg_growth

            try:
                # res.pop('MSTD_errors')
                res.pop('starting_states')
                res.pop('episode_durations')
                #res.pop('episode_returns')
                res.pop('skip_run_episodes')
                res.pop('stepsize')
                res.pop('final_performance')
            except:
                print(f'WARNING: seems like {res_json_file} is incomplete')
                continue

            if res['experience_replay_capacity'] == 10000:
                if res['target_network'] == 2:
                    tricks_key = 'both_tricks'
                else:
                    tricks_key = 'experience_replay'
            else:
                if res['target_network'] == 2:
                    tricks_key = 'target_network_fixing'
                else:
                    tricks_key = 'no_tricks'


            # tricks_key = 'Replay_' + str(res['experience_replay_capacity']) + '__Target_' + str(res['target_network'])

            result_list[res['environment_name']][tricks_key][res['seed']].append(res)

    return result_list

def create_avg_over_seeds(result_list):
    print("\n Now creating seed avgs \n")
    best_hyperparameters = {}

    for env, env_results in result_list.items():
        best_hyperparameters[env] = {}
        trick_returns = defaultdict(dict)
        trick_returns_std = defaultdict(dict)
        upper, lower = None, None
        upper_mstd, lower_mstd = None, None

        for tricks_key, trick_results in env_results.items():

            print(f"Now running for {env} + {tricks_key} \n")
            MSTD_errors = []
            returns = defaultdict(dict)
            returns_std = defaultdict(dict)
            returns_for_avg = []


            heatmap_running = defaultdict(lambda: defaultdict(list))
            MSTDE_growth_running = defaultdict(lambda: defaultdict(list))

            heatmap_data = []
            MSTDE_growth = []

            avg_arr = None
            avg_arr_MSTDE = None


            for seed, seed_res in trick_results.items():
                avg_perf = []
                avg_perf_MSTDE = []

                for run_res in seed_res:
                    avg_perf.append(run_res['avg_final_performance'])
                    avg_perf_MSTDE.append(run_res['avg_growth'])


                    heatmap_running[run_res['eps_min']][run_res['discount_factor']].append([
                        run_res['avg_final_performance'],
                        # run_res['avg_growth']
                    ])


                    MSTDE_growth_running[run_res['eps_min']][run_res['discount_factor']].append([
                        # run_res['MSTD_errors'],
                        run_res['avg_growth']
                    ])

                    # TODO this means we are taking the final hyper parameter combination of the seed. this should be the best!!!
                    returns[seed] = [{'x': x, 'y': y} for x, y in enumerate(run_res['episode_returns'])]

                    # TODO here we are appending all episode returns, which should also be the best only
                    returns_for_avg.append(run_res['episode_returns'])

                if avg_arr is None:
                    avg_arr = np.array(avg_perf)
                else:
                    avg_arr += np.array(avg_perf)


                if avg_arr_MSTDE is None:
                    avg_arr_MSTDE = np.array(avg_perf_MSTDE)
                else:
                    avg_arr_MSTDE += np.array(avg_perf_MSTDE)


            # print(avg_arr)
            perf_upp = (avg_arr/5).max()
            best_perf = avg_arr.argmax()

            # input(len(returns_for_avg))
            # input(len(returns_for_avg[best_perf*5 : best_perf*5+5]))
            # returns_for_avg = returns_for_avg[best_perf*5 : best_perf*5+5]

            best_eps = 0.05 * (1 + best_perf % 7)
            best_gam = 0.7 + 0.05 * (best_perf // 7)

            best_hyperparameters[env][tricks_key] = {"eps": best_eps, "gam": best_gam, "res": perf_upp}
            # print(best_perf, avg_arr[best_perf]/5)
            # print(f"best epsilon: {best_eps}, best gamma: {best_gam}")
            # input()
            perf_low = (avg_arr/5).min()

            if upper is not None:
                if upper < perf_upp:
                    upper = perf_upp
            else:
                upper = perf_upp

            if lower is not None:
                if lower > perf_low:
                    lower = perf_low
            else:
                lower = perf_low

            # TODO, yea, if this breaks we have inconsistent numbers of episodes
            returns_std_for_avg = np.std(np.array(returns_for_avg), axis=0)
            returns_for_avg = np.mean(np.array(returns_for_avg), axis=0)

            trick_returns[tricks_key] = [{'x': x, 'y': y} for x, y in enumerate(list(returns_for_avg))]
            trick_returns_std[tricks_key] = [{'x': x, 'y': y} for x, y in enumerate(list(returns_std_for_avg))]

            for epsilon, discount_factors in heatmap_running.items():
                for discount_factor, values in discount_factors.items():
                    values = np.array(values)

                    # print(len(values), values)
                    # input()
                    heatmap_data.append({
                        'discount_factor': round(discount_factor, 2),
                        'epsilon': round(epsilon, 2),
                        'return': round(sum(values[:, 0])/len(values[:, 0]), 2),
                        # 'growth': round(sum(values[:, 1])/len(values[:, 1]), 2)
                    })



            for epsilon, discount_factors in MSTDE_growth_running.items():
                for discount_factor, values in discount_factors.items():
                    values = np.array(values)

                    # running_mean_MSTDE = 0.0
                    # n_train_seeds = 5
                    # for seed_idx in range(n_train_seeds):
                    #     # print((np.array(values[seed_idx][0][1:])/np.array(values[seed_idx][0][:-1])).shape)
                    #     # print(np.array(values[seed_idx][0][-2:-1]).shape)
                    #     # input()
                    #     running_mean_MSTDE += 1/n_train_seeds * np.sum(np.log(np.array(values[seed_idx][0][-1:])/np.array(values[seed_idx][0][-2:-1])))/(len(values) - 1)
                    #

                    # print(len(values), values)
                    # input()
                    running_mean_MSTDE = round(sum(values[:, 0])/len(values[:, 0]), 2)


                    MSTDE_growth.append({
                        'discount_factor': round(discount_factor, 2),
                        'epsilon': round(epsilon, 2),
                        'return': running_mean_MSTDE
                        # 'growth': round(sum(values[:, 1])/len(values[:, 1]), 2)
                    })


                    # if upper_mstd is not None:
                    #     if upper_mstd < running_mean_MSTDE:
                    #         upper_mstd = running_mean_MSTDE
                    # else:
                    #     upper_mstd = running_mean_MSTDE
                    #
                    # if lower_mstd is not None:
                    #     if lower_mstd > running_mean_MSTDE:
                    #         lower_mstd = running_mean_MSTDE
                    # else:
                    #     lower_mstd = running_mean_MSTDE

            # result_list[env][tricks_key]['MSTD_errors'] = MSTD_errors
            result_list[env][tricks_key] = {
                'returns': {'data': returns},
                'grid_search': heatmap_data,
                'mstd_grid': MSTDE_growth
            }


        result_list[env]['heatmap_bounds'] = {'upper': upper, 'lower': lower}
        # result_list[env]['heatmap_bounds'].update({'Qupper_mstd': upper_mstd, 'Qlower_mstd': lower_mstd})

        result_list[env]["all_tricks"] = {
            'returns': {"data": trick_returns, 'std': trick_returns_std}}

        result_list[env]["best_runs"] = best_hyperparameters[env]

    for env in best_hyperparameters:
        for tricks in best_hyperparameters[env]:
            print(env, tricks, best_hyperparameters[env][tricks])

    return result_list

if __name__ == '__main__':
    results = create_avg_over_seeds(group_results())
    with open('results/processed_data.json', 'w') as f:
        json.dump(results, f)

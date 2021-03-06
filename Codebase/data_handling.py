import json
import os
import torch
import time
import numpy as np

class DataHandler:
    def __init__(self, args):
        self.args = args
        # These should not have any influence on where the model/data are saved/loaded
        self.excluded_parameters = ['pretrained', 'do_not_train', 'create_animation', 'skip_run_episodes', 'environment_name']
        self.envdir = args.environment_name
        self.resdir = self.results_dir = self.__settings_to_resdir(vars(self.args))

    def __settings_to_resdir(self, datadict):
        """ Returns the appropriate results directory for the given settings"""
        resdir = ",".join(sorted([k[0] + str(v) for k, v in datadict.items() if k not in self.excluded_parameters]))
        return os.path.join("results", self.envdir,  resdir)


    @staticmethod
    def __dict_match(filter, dictionary):
        """checks whether all key value pairs in the filter.

        Parameters
        ----------
        filter : dict
            key, value pairs required to be in a dictionary
        dictionary : type
            Description of parameter `dictionary`.

        Returns
        -------
        Bool
            True when all values in the filter occur in the given dictionary
            False when there is any mismatch between the filter and the dictionary
        """
        for k, v in filter.items():
            if not dictionary[k] == v:
                return False
        return True

    def load_model(self):
        """
        Tries to find a pretrained Q-network for the current settings

        Parameters
        ----------
        args : Namespace
            output of argparse.
        Returns
        -------
        DQN
        """

        if not self.args.save_network:
            raise ValueError("Looks like you are trying to load a pretrained model without the --save_network flag. \
                              This means there is likely no pretrained model for the given settings.")

        if not os.path.isdir(self.resdir):
            raise ValueError(f"Could not find results directory '{self.resdir}'. Try running without the --pretrained flag to create it")

        modelpath = os.path.join(self.resdir, 'Q.pt')

        if not os.path.isfile(modelpath):
            raise ValueError(f"Could not find Q network in {modelpath}. Something might have gone wrong while saving the model")

        return torch.load(modelpath)


    def save_data(self, episode_durations, episode_returns, starting_states, Q, MSTD_errors, performances):
        """saves a json with run results and properties of a run, like
        hyperparameters, environment etc.

        load results with load_data()

        Parameters
        ----------
        episode_durations : list of ints
            number of steps per epsiode
        episode_returns : list of rewards, depends on environment
            total reward (undiscounted) per episode
        starting_states : list of starting starting_states per episode

        Returns
        -------
        None
        """
        datadict = vars(self.args)
        envdir = self.envdir
        resdir = self.resdir


        datadict["episode_durations"] = episode_durations
        datadict["episode_returns"] = episode_returns
        datadict["starting_states"] = starting_states
        datadict["MSTD_errors"] = [x.item() for x in MSTD_errors]
        datadict["final_performance"] = performances
        datadict["avg_final_performance"] = np.mean(performances).item()
        print(datadict)

        if not os.path.exists("results"):
            os.mkdir("results")

        if not os.path.exists(os.path.join("results", envdir)):
            os.mkdir(os.path.join("results", envdir))

        if not os.path.exists(resdir):
            os.mkdir(resdir)

        if self.args.save_network:
            torch.save(Q, os.path.join(resdir, 'Q.pt'))

        with open(os.path.join(resdir, 'results.json'), "w+") as f:
            json.dump(datadict, f, indent=4)


    @staticmethod
    def load_data(filter=None):
        """loads in all the result files.

        Returns list of dictionaries with run properties like environment,
        hyperparameters & tricks.

        Using filter returns only those dictionaries where the properties
        correspond to the filter.

        example usage:

        load_data(filter={'environment_name':'Acrobot-v1', 'epsilon':0.05})

        Parameters
        ----------
        filter : dictionary
            properties like in the argparse


        Returns
        -------
        list of dictionaries
            Description of returned object.

        """
        r_dirs = [os.path.join('results', f) for f in os.listdir("results") if os.path.isdir(os.path.join("results", f))]
        jsons = []
        for rdir in r_dirs:
            # print("rdir",rdir)
            for d in os.listdir(rdir):
                # print(d)
                # print(os.path.exists(os.path.join(rdir, d)))
                # print([f for f in os.listdir(os.path.join(rdir, d)) if os.path.splitext(f)[1] == '.json'])
                for f in os.listdir(os.path.join(rdir, d)):
                    if os.path.isfile(os.path.join(os.path.join(rdir, d), f)) and os.path.splitext(f)[1] == '.json':
                        jsons += [json.load(open(os.path.join(os.path.join(rdir, d), f), "r"))]

        if not (filter is None):
            filtered_jsons = []
            for result_json in jsons:
                if DataHandler.__dict_match(filter, result_json):
                    filtered_jsons.append(result_json)
            filtered_jsons = [result_json for result_json in jsons if DataHandler.__dict_match(filter, result_json)]
            return filtered_jsons
        else:
            return jsons

    def save_animation(self, animation):
        s = time.time()
        animation.save(os.path.join(self.resdir, 'animation.mp4'), fps=30)
        print("took", time.time() - s)

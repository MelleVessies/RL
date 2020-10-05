import json
import os


def save_data(args, episode_durations, episode_returns, starting_states):
    """saves a json with run results and properties of a run, like
    hyperparameters, environment etc.

    load results with load_data()



    Parameters
    ----------
    args : Namespace
        output of argparse.
    episode_durations : list of ints
        number of steps per epsiode
    episode_returns : list of rewards, depends on environment
        total reward (undiscounted) per episode
    starting_states : list of starting starting_states per episode

    Returns
    -------
    None
    """
    datadict = vars(args)
    fname = ",".join(sorted([k[0] + str(v) for k,v in datadict.items()]))

    datadict["episode_durations"] = episode_durations
    datadict["episode_returns"] = episode_returns
    datadict["starting_states"] = starting_states

    if not os.path.exists("results"):
        os.mkdir("results")


    with open(os.path.join("results", fname), "w+") as f:
        json.dump(datadict, f, indent=4)


def dict_match(filter, dictionary):
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
    for k,v in filter.items():
        if not (dictionary[k] == v):
            return False
    return True


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
    result_files = [f for f in os.listdir("results") if os.path.isfile(os.path.join("results", f))]
    jsons = [json.load(open(os.path.join("results", f), "r")) for f in result_files]

    if not (filter is None):
        filtered_jsons = [result_json for result_json in jsons if dict_match(filter, result_json)]
        return filtered_jsons
    else:
        return jsons

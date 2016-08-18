import numpy as np
from multiprocessing import cpu_count
from os.path import exists
from os import mkdir
from datetime import datetime
import platform
from module.simulation_manager import Launcher
from module.save_eco import BackUp


def date():

    return str(datetime.now())[:-10].replace(" ", "_").replace(":", "-")


def simple_run(logs=True):

    t_max = 500
    workforce = np.array([50, 50, 100], dtype=int)
    model = "BG"
    model_parameters = "economics-model-parameters.json"
    hebbian = False
    reward_amount = 1

    root_folder = "../single_shot_data"

    if not exists(root_folder):

        mkdir(root_folder)

    if logs:

        logs_folder = "../single_shot_logs"
        if not exists(logs_folder):
            mkdir(logs_folder)

    param = \
        {
            "workforce": workforce,
            "t_max": t_max,  # Set the number of time units the simulation will run.
            "cpu_count": cpu_count(),
            "model": model,
            "model_parameters": model_parameters,
            "hebbian": hebbian,
            "reward_amount": reward_amount,
            "date": date(),
            "idx": np.random.randint(99999)
        }

    if logs:
        results = Launcher.launch(param, single=False)
    else:
        results = Launcher.launch(param, single=True)

    BackUp.save_data(results=results, parameters=param, root_folder=root_folder)


if __name__ == "__main__":

    # If on mac platform suppose that no log files are needed
    if platform == "Darwin":

        simple_run(logs=False)
    else:

        simple_run(logs=True)

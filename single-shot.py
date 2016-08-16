import numpy as np
from multiprocessing import cpu_count
from os.path import exists
from os import mkdir
from datetime import datetime
from module.simulation_manager import Launcher
from module.save_eco import BackUp


def date():

    return str(datetime.now())[:-10].replace(" ", "_").replace(":", "-")


def simple_run(logs=True):

    t_max = 20000
    workforce = np.array([50, 50, 100], dtype=int)
    model = "BG"
    model_parameters = "model-topalidou-august-parameters.json"

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
            "hebbian": True,
            "date": date(),
            "idx": np.random.randint(99999)
        }

    results = Launcher.launch(param, single=False)
    BackUp.save_data(results=results, parameters=param, root_folder=root_folder)


if __name__ == "__main__":

    simple_run(logs=True)

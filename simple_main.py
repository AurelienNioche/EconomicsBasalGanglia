import numpy as np
from multiprocessing import cpu_count
from os.path import exists
from os import mkdir
from module.SimulationManager import Launcher
from module.save_eco import BackUp


def simple_run(logs=True):

    t_max = 10000
    model = "BG"

    root_folder = "../single_shot_data"

    if not exists(root_folder):

        mkdir(root_folder)

    if logs:

        logs_folder = "../single_shot_logs"
        if not exists(logs_folder):
            mkdir(logs_folder)

    param = \
        {
            "workforce": np.array([50, 50, 100], dtype=int),
            "t_max": t_max,  # Set the number of time units the simulation will run.
            "cpu_count": 12,
            "model": model,
            "date": "example",
            "idx": 0
        }

    results = Launcher.launch(param)
    BackUp.save_data(results=results, parameters=param, root_folder=root_folder)


if __name__ == "__main__":

    simple_run()

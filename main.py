import pickle
import argparse
from module.SimulationManager import Launcher
from module.save_eco import BackUp


def get_parameters():

    parser = argparse.ArgumentParser()

    parser.add_argument('parameters', type=str,
                        help='A name of pickle file for parameters is required!')

    args = parser.parse_args()

    pickle_file = args.parameters

    parameters = pickle.load(open(pickle_file, mode='rb'))

    return parameters


def main():

    parameters = get_parameters()
    results = Launcher.launch(parameters, single=False)
    BackUp.save_data(results=results, parameters=parameters)


if __name__ == "__main__":

    main()
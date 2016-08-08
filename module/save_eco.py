from pickle import dump
from os import path, mkdir


class BackUp(object):

    @classmethod
    def save_data(cls, results, parameters):

        cls.create_folders()

        print("\nSaving data...")

        saving_name = "{date}_idx{idx}".format(date=parameters["date"], idx=parameters["idx"])

        direct_exchanges = results["direct_exchanges"]
        indirect_exchanges = results["indirect_exchanges"]

        dump(direct_exchanges,
             open("../data/exchanges/direct_exchanges_{}.p".format(saving_name), mode='wb'))

        dump(indirect_exchanges,
             open("../data/exchanges/indirect_exchanges_{}.p".format(saving_name), mode='wb'))

        dump(parameters,
             open("../data/parameters/parameters_{}.p".format(saving_name), mode='wb'))

        print("\nData saved...")

    @classmethod
    def create_folders(cls):

        folders = ["../data", "../data/parameters", "../data/exchanges"]
        for i in folders:

            if not path.exists(i):

                mkdir(i)

import pickle
from pylab import np, plt
from os import listdir, mkdir
from os.path import isfile, join, exists
from tqdm import tqdm


class DataImporter(object):

    def __init__(self, data_folder):

        assert exists(data_folder), "Wrong name for data folder..."

        self.folder = {
            "parameters": "{}/parameters".format(data_folder),
            "exchanges": "{}/exchanges".format(data_folder)
        }

    def import_suffix_list(self):

        mypath = self.folder["parameters"]
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        suffixes = [f.split("parameters_")[1] for f in onlyfiles]
        return suffixes

    def import_data_for_single_session(self, session_suffix):

        parameters = pickle.load(
            open("{}/parameters_{}".format(self.folder["parameters"], session_suffix), mode='rb'))
        # print("parameters", parameters)

        indirect_exchanges = pickle.load(
            open("{}/indirect_exchanges_{}".format(self.folder["exchanges"], session_suffix), mode='rb'))

        direct_exchanges = pickle.load(
            open("{}/direct_exchanges_{}".format(self.folder["exchanges"], session_suffix), mode='rb'))

        return {"parameters": parameters, "indirect_exchanges": indirect_exchanges,
                "direct_exchanges": direct_exchanges}


class Analysis(object):

    @classmethod
    def simple_analysis(cls, indirect_exchange, figure_folder, msg="", suffix=""):

        cls.plot(indirect_exchange, figure_folder, msg=msg, suffix=suffix)

    @classmethod
    def plot(cls, data, figure_folder, msg="", suffix=""):

        x = np.arange(len(data[:]))

        plt.plot(x, data[:, 0], c="red", linewidth=2)
        plt.plot(x, data[:, 1], c="blue", linewidth=2)
        plt.plot(x, data[:, 2], c="green", linewidth=2)
        plt.ylim([-0.01, 1.01])
        plt.text(0, -0.12, "{}".format(msg))

        if not exists(figure_folder):
            mkdir(figure_folder)
        fig_name = "{}/figure_{}.pdf".format(figure_folder, suffix.split(".p")[0])
        plt.savefig(fig_name)
        plt.close()


def main():

    single = 0
    if single:

        # data_folder = "/users/M-E4-ANIOCHE/Desktop/single_shot_data"
        # figure_folder = "/users/M-E4-ANIOCHE/Desktop/single_shot_figures"

        data_folder = "../single_shot_data"
        figure_folder = "../single_shot_figures"

    else:

        data_folder = "/users/M-E4-ANIOCHE/Desktop/data"
        figure_folder = "/users/M-E4-ANIOCHE/Desktop/figures"
        # data_folder = "../data-batch4"
        # figure_folder = "../figures-batch4"

    data_importer = DataImporter(data_folder=data_folder)

    suffixes = data_importer.import_suffix_list()

    for suffix in tqdm(suffixes):

        data = data_importer.import_data_for_single_session(suffix)

        try:

            msg = "workforce: {}, t_max: {}, hebbian: {}, \nparameters: {}"\
                .format(data["parameters"]["workforce"],
                        data["parameters"]["t_max"],
                        data["parameters"]["hebbian"],
                        data["parameters"]["model_parameters"])

        except KeyError:

            msg = "workforce: {}, t_max: {}, \nparameters: {}" \
                .format(data["parameters"]["workforce"],
                        data["parameters"]["t_max"],
                        data["parameters"]["model_parameters"])

        Analysis.simple_analysis(data["indirect_exchanges"], figure_folder=figure_folder, msg=msg, suffix=suffix)


if __name__ == "__main__":

    # Analysis.simple_analysis(results_folder="../data", session_suffix="example_idx0")
    main()


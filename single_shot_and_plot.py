from pylab import plt, np
from multiprocessing import cpu_count
from module.simulation_manager import Launcher


class Analysis(object):

    @classmethod
    def simple_analysis(cls, indirect_exchange, msg=""):

        cls.plot(indirect_exchange, msg=msg)

    @classmethod
    def plot(cls, data, msg=""):

        x = np.arange(len(data[:]))

        plt.plot(x, data[:, 0], c="red", linewidth=2)
        plt.plot(x, data[:, 1], c="blue", linewidth=2)
        plt.plot(x, data[:, 2], c="green", linewidth=2)
        plt.ylim([-0.01, 1.01])
        plt.text(0, -0.12, "{}".format(msg))

        plt.show()
        #if not exists(figure_folder):
        #    mkdir(figure_folder)
        #fig_name = "{}/figure_{}.pdf".format(figure_folder, suffix.split(".p")[0])
        #plt.savefig(fig_name)
        #plt.close()


def simple_run():

    t_max = 40
    workforce = np.array([5, 5, 15], dtype=int)
    model = "BG"
    model_parameters = "economics-model-parameters.json"
    hebbian = False
    reward_amount = 2

    param = \
        {
            "workforce": workforce,
            "t_max": t_max,  # Set the number of time units the simulation will run.
            "cpu_count": cpu_count(),
            "model": model,
            "model_parameters": model_parameters,
            "hebbian": hebbian,
            "reward_amount": reward_amount
        }

    results = Launcher.launch(param, single=True)

    msg = "workforce: {}, t_max: {}, hebbian: {}, \nparameters: {}" \
        .format(param["workforce"],
                param["t_max"],
                param["hebbian"],
                param["model_parameters"])

    Analysis.simple_analysis(results["indirect_exchanges"], msg=msg)


if __name__ == "__main__":

    simple_run()

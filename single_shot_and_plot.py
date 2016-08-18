from pylab import plt, np
from platform import system
import json
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


def simple_run():

    param = json.load(open("simple-shot-and-plot-parameters.json", mode="r"))

    param["cpu_count"] = cpu_count()
    param["model"] = "BG"

    results = Launcher.launch(param, single=True)

    msg = "workforce: {}, t_max: {}, hebbian: {}, \nparameters: {}" \
        .format(param["workforce"],
                param["t_max"],
                param["hebbian"],
                param["model_parameters"])

    Analysis.simple_analysis(results["indirect_exchanges"], msg=msg)


if __name__ == "__main__":

    if system() == 'Lunix':

        # Test visual output
        plt.plot(np.arange(10), np.arange(10))
        plt.show()

    simple_run()

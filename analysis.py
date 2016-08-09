import pickle
from pylab import np, plt


def simple_analysis(results_folder, session_suffix):

    parameters = pickle.load(open("{}/parameters/parameters_{}.p".format(results_folder, session_suffix), mode='rb'))
    print("parameters", parameters)

    data = pickle.load(open("{}/exchanges/indirect_exchanges_{}.p".format(results_folder, session_suffix), mode='rb'))

    x = np.arange(len(data[:]))

    plt.plot(x, data[:, 0], c="red", linewidth=2)
    plt.plot(x, data[:, 1], c="blue", linewidth=2)
    plt.plot(x, data[:, 2], c="green", linewidth=2)
    plt.ylim([-0.01, 1.01])

    plt.show()


if __name__ == "__main__":

    simple_analysis(results_folder="../data", session_suffix="example_idx0")


import numpy as np
from time import sleep
from tqdm import tqdm
from pylab import plt
from module.BGModel import Model


def main():

    model = Model(filename="model-topalidou.json")

    results_mot = []
    results_cog = []

    t_max = 500

    for i in tqdm(range(t_max)):

        choice = model.choose(
            possible_moves=np.array([1, 1, 0, 0], dtype=float),
            possible_strategies=np.ones(4)
        )

        results_cog.append(choice["cog"])
        results_mot.append(choice["mot"])

        # model.learn(np.random.randint(2))
        if choice["mot"] == 0:
            model.learn(reward=0)
        else:
            model.learn(reward=1)

    sleep(0.1)
    print()

    print("Cog results: ",
          "0:", results_cog.count(0)/len(results_cog),
          "; 1:", results_cog.count(1) / len(results_cog),
          "; 2:", results_cog.count(2) / len(results_cog),
          "; 3:", results_cog.count(3) / len(results_cog),
          "; -1:", results_cog.count(-1) / len(results_cog))

    print("Mot results: ",
          "0:", results_mot.count(0)/len(results_mot),
          "; 1:", results_mot.count(1) / len(results_mot),
          "; 2:", results_mot.count(2) / len(results_mot),
          "; 3:", results_mot.count(3) / len(results_mot),
          "; -1:", results_mot.count(-1) / len(results_mot))

    plot(results_mot)


def plot(mot_results):

    bool_mot_results = np.asarray(mot_results) == 1

    t_max = len(bool_mot_results)

    average_t = np.zeros(t_max)

    time_window = 10

    for t in range(t_max):

        if t < time_window:
            average_t[t] = np.mean(bool_mot_results[:t+1])
        else:
            average_t[t] = np.mean(bool_mot_results[t-10:t+1])

    try:
        plt.plot(np.arange(t_max), average_t, linewidth=2)
        plt.ylim([-0.01, 1.01])
        plt.show("figure.pdf")
    except:
        print("Could not show the figure but here are the results:")
        print(average_t)


if __name__ == "__main__":

    main()


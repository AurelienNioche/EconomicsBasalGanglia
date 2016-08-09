import numpy as np


class RLAgent(object):

    def __init__(self):

        self.strategy = None

        self.tau = 0.01
        self.alpha = 0.02

        self.strategies = \
            np.array([[1., 0., 1., 0.],
                      [1., 0., 0., 1.],
                      [0., 1., 1., 0.],
                      [0., 1., 0., 1.]])

        self.n_strategies = 4

        self.values = np.ones(self.n_strategies) * 0.5

        self.choice = {"cog": 0, "mot": 0}

        self.name = np.random.randint(1000, 9999)

    def choose(self, possible_choices):

        self.choose_strategy()

        self.choice["mot"] = np.argmax(possible_choices * self.strategies[self.strategy])
        self.choice["cog"] = self.strategy

        return self.choice

    def learn(self, reward):

        if reward is not None:

            self.values[self.strategy] += self.alpha * (reward - self.values[self.strategy])

    def choose_strategy(self):

        denominator = np.sum(np.exp(self.values[:]/self.tau))

        p_values = np.zeros(self.n_strategies)

        p_values[:] = np.exp(self.values[:]/self.tau)/denominator

        self.strategy = np.random.choice(np.arange(self.n_strategies), p=p_values)

import numpy as np
from time import time
from multiprocessing import Pool, cpu_count
from module.RLModel import RLAgent


class RLAgentsManager(object):

    def __init__(self, parameters):

        self.model = RLAgent
        self.agents = None

        self.n = np.sum(parameters["workforce"])  # Total number of agents

        self.workforce = np.zeros(len(parameters["workforce"]), dtype=int)
        self.workforce[:] = parameters["workforce"]  # Number of agents by type

        self.type = np.zeros(self.n, dtype=int)

        self.type[:] = np.concatenate(([0, ] * self.workforce[0],
                                       [1, ] * self.workforce[1],
                                       [2, ] * self.workforce[2]))

        self.possible_strategies = \
            np.array([[1, 0, 1, 0],
                      [1, 0, 0, 1],
                      [0, 1, 1, 0],
                      [0, 1, 0, 1]])

        self.timers = dict()
        for i in ["choose", "teach"]:

            self.timers[i] = {"call": 0, "time": 0}

        # self.choices = Array("i", size_or_initializer=range(self.n))
        self.choices = np.zeros(self.n, dtype=int)
        self.id_decision0 = None
        self.id_decision1 = None

        self.possibilities = [np.array([1., 1., 0., 0.]), np.array([0., 0., 1., 1.])]

        self.pool = Pool(processes=cpu_count())

    def create_agents(self):

        self.agents = np.zeros(self.n, dtype=self.model)

        for i in range(self.n):
            self.agents[i] = self.model()
            self.agents[i].set_possible_strategies(self.possible_strategies)

    def have_agents_choose(self, decision_array):

        self.timers["choose"]["call"] += 1
        a = time()

        '''
            :param id_decision_0: indexes of agents facing a type-0 decision
            :param id_decision_1: indexes of agents facing a type-1 decision
            :return: an array of size n with values in [0, 1]
        '''

        for i, decision in enumerate(decision_array):

            possible_choices = self.possibilities[decision]
            dic_choice = self.agents[i].choose(possible_choices)
            mot_choice = dic_choice["mot"] - 2 * decision

            # assert mot_choice in [0, 1]
            self.choices[i] = mot_choice

        b = time()
        self.timers["choose"]["time"] += b-a

        return self.choices

    def teach_agents(self, success_id):

        self.timers["teach"]["call"] += 1
        a = time()

        for i in success_id:

            self.agents[i].learn(1)

        cplt_success = np.setdiff1d(np.arange(self.n), success_id)

        for i in cplt_success:

            self.agents[i].learn(0)

        b = time()
        self.timers["teach"]["time"] += b - a

    def quit(self):

        pass

    def __del__(self):

        print("Execution times:", self.timers)

    @classmethod
    def test_agents_manager(cls):

        i, j, k = 250, 250, 250
        parameters = {"workforce": np.array([i, j, k], dtype=int)}
        agent_manager = RLAgentsManager(parameters=parameters)
        agent_manager.create_agents()

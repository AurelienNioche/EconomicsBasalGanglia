import numpy as np


class RLAgent(object):

    def __init__(self):

        self.strategies = None
        self.n_strategies = None

        self.values = None
        self.strategy = None

        self.tau = 0.01
        self.alpha = 0.02

        self.choice = {"cog": 0, "mot": 0}

        self.name = np.random.randint(1000, 9999)

    def set_possible_strategies(self, possible_strategies):

        self.strategies = np.asarray(possible_strategies, dtype=bool)
        self.n_strategies = len(possible_strategies)
        self.values = np.ones(self.n_strategies) * 0.5

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

        self.choices = np.zeros(self.n, dtype=int)
        self.id_decision0 = None
        self.id_decision1 = None

        self.possibilities = [np.array([1., 1., 0., 0.]), np.array([0., 0., 1., 1.])]

    def create_agents(self):

        self.agents = np.zeros(self.n, dtype=self.model)

        for i in range(self.n):
            self.agents[i] = self.model()
            self.agents[i].set_possible_strategies(self.possible_strategies)

    def have_agents_choose(self, id_decision_0, id_decision_1):

        '''
            :param id_decision_0: indexes of agents facing a type-0 decision
            :param id_decision_1: indexes of agents facing a type-1 decision
            :return: an array of size n with values in [0, 1]
        '''

        arg_for_workers = []

        for i in id_decision_0:

            arg_for_workers.append({"decision": 0,
                                    'idx': i})

        for j in id_decision_1:

            arg_for_workers.append({"decision": 1,
                                    'idx': j})

        for i in map(self.choice_function, arg_for_workers):

            self.choice_function(arg_for_workers)

        return self.choices

    def choice_function(self, kwargs):

        idx = kwargs["idx"]
        dec = kwargs["decision"]

        possible_choices = self.possibilities[dec]

        dic_choice = {"mot": None, "cog": None}

        response = False
        while not response:
            dic_choice = self.agents[idx].choose(possible_choices)
            response = dic_choice["mot"] != -1

        mot_choice = dic_choice["mot"] - 2*dec
        assert mot_choice in [0, 1]
        self.choices[idx] = mot_choice

    def teach_agents(self, success_id):

        for i in success_id:

            self.agents[i].learn(1)

        cplt_success = np.setdiff1d(np.arange(self.n), success_id)

        for i in cplt_success:

            self.agents[i].learn(0)

    @classmethod
    def test_agents_manager(cls):

        i, j, k = 250, 250, 250
        parameters = {"workforce": np.array([i, j, k], dtype=int)}
        agent_manager = RLAgentsManager(parameters=parameters)
        agent_manager.create_agents()

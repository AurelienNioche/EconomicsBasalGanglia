import numpy as np
from time import time
from multiprocessing import Process, Queue, Event, cpu_count
from tqdm import tqdm
from module.BGModel import Model as BGModel


class EcoProcess(Process):

    def __init__(self, **kwargs):

        Process.__init__(self)
        self.demand_queue = kwargs["demand_queue"]
        self.result_queue = kwargs["result_queue"]
        self.stop = kwargs["stop"]
        self.model_parameters = kwargs["model_parameters"]
        self.hebbian = kwargs["hebbian"]
        self.n = kwargs["n"]
        self.reward_amount = 2
        self.possibilities = [np.array([1., 1., 0., 0.]), np.array([0., 0., 1., 1.])]

    def run(self):

        # Create agents
        agents = self.create_agents()

        # Enter in the loop
        while not self.stop.is_set():

            # Wait for demand
            p_choices = self.demand_queue.get()

            if p_choices is not None:

                ############################
                #       CHOICE             #
                ############################

                # Have the model choose
                choices = []
                for i in range(self.n):

                    possible_choices = self.possibilities[p_choices[i]]

                    choice = agents[i].choose(possible_moves=possible_choices)

                    while choice["mot"] == -1:
                        choice = agents[i].choose(possible_moves=possible_choices)

                    choices.append(choice)

                # Each agent has chosen

                self.result_queue.put(choices)

                ################################
                #       LEARNING               #
                ################################

                success = self.demand_queue.get()
                for i in range(self.n):

                    agents[i].learn(success[i]*self.reward_amount)
            else:
                pass

    def create_agents(self):

        agents = []

        for i in range(self.n):

            model = BGModel(filename=self.model_parameters,
                            hebbian=self.hebbian)
            agents.append(model)

        return agents


class BGAgentsManager(object):

    def __init__(self, parameters):

        self.model = BGModel

        self.model_parameters = parameters["model_parameters"]
        self.hebbian = parameters["hebbian"]

        self.n = np.sum(parameters["workforce"])  # Total number of agents

        self.n_workers = parameters["cpu_count"]
        self.n_agents_by_worker = np.zeros(self.n_workers, dtype=int)

        self.demand_queues = [Queue() for i in range(self.n_workers)]
        self.result_queues = [Queue() for i in range(self.n_workers)]
        self.stop_signal = Event()

        self.choices = np.zeros(self.n)

        self.timers = dict()
        for i in ["choose", "teach"]:

            self.timers[i] = {"call": 0, "time": 0}

        # self.choices = Array("i", size_or_initializer=range(self.n))
        self.choices = np.zeros(self.n, dtype=int)
        self.id_decision0 = None
        self.id_decision1 = None

    def create_agents(self):

        self.n_agents_by_worker[:] = int(self.n/self.n_workers)
        reminder = self.n % self.n_workers

        # Distribute a certain number of agents among the workers
        while reminder > 0:

            for i in range(self.n_workers):

                self.n_agents_by_worker[i] += 1
                reminder -= 1

                if reminder > 0:

                    continue

                else:

                    break

        print("Repartition of work between workers:", self.n_agents_by_worker)

        for i, n in enumerate(self.n_agents_by_worker):

            p = EcoProcess(demand_queue=self.demand_queues[i],
                           result_queue=self.result_queues[i],
                           stop=self.stop_signal,
                           model_parameters=self.model_parameters,
                           hebbian=self.hebbian,
                           n=n)
            p.start()

    def have_agents_choose(self, decision_array):

        self.timers["choose"]["call"] += 1
        a = time()

        '''
            :param id_decision_0: indexes of agents facing a type-0 decision
            :param id_decision_1: indexes of agents facing a type-1 decision
            :return: an array of size n with values in [0, 1]
        '''

        cursor = 0
        for i in range(self.n_workers):

            j = self.n_agents_by_worker[i]

            self.demand_queues[i].put(decision_array[cursor: cursor+j])
            cursor += j

        cursor = 0
        for i in range(self.n_workers):
            j = self.n_agents_by_worker[i]

            r = self.result_queues[i].get()

            self.choices[cursor: cursor+j] = [i["mot"] for i in r]
            cursor += j

        self.choices[:] = self.choices - (decision_array*2)

        b = time()
        self.timers["choose"]["time"] += b-a

        return self.choices

    def quit(self):

        self.stop_signal.set()

        for i in range(self.n_workers):

            self.demand_queues[i].put(None)

        print("Execution times:", self.timers)

    def teach_agents(self, success_id):

        self.timers["teach"]["call"] += 1
        a = time()

        success_array = np.zeros(self.n)
        success_array[success_id] = 1

        cursor = 0
        for i in range(self.n_workers):

            j = self.n_agents_by_worker[i]

            self.demand_queues[i].put(success_array[cursor: cursor + j])
            cursor += j

        b = time()
        self.timers["teach"]["time"] += b - a


def agent_manager_main():

    # Simple example with multiprocessing but without real economic environment

    print("Test the management of multiple agents...")
    a = time()

    workforce = np.array([100, 100, 100])
    t_max = 100
    parameters = \
        {"workforce": workforce,
         "cpu_count": cpu_count()}

    n = workforce.sum()

    agent_manager = BGAgentsManager(parameters=parameters)
    agent_manager.create_agents()

    # Keep motor choices
    motor_choices = []

    for i in tqdm(range(t_max)):

        # Have agents choose, making them face randomly a decision '0' or '1'
        decision_idx = np.random.randint(0, 2, size=n)
        choices = agent_manager.have_agents_choose(decision_array=decision_idx)

        # Keep a trace of motor choices
        motor_choices += list(choices)

        # Give a good response to 40% of agents, randomly chosen
        successful_idx = np.random.choice(np.arange(n), size=int(0.4/n), replace=False)
        agent_manager.teach_agents(success_id=successful_idx)

    agent_manager.quit()

    print("Fake results:",
          "p0", motor_choices.count(0)/len(motor_choices),
          "; p1", motor_choices.count(1)/len(motor_choices))

    b = time()
    print("Global time:", b-a)

    print()


def simple_main():

    # Test a unique agent to be sure that everything is working as expected

    print("Test a single agent...")

    model = BGModel()

    choice = model.choose(possible_moves=np.array([1., 1., 0., 0.]))

    print("Agent choice:", choice)
    print()


if __name__ == "__main__":

    # Does a single agent can make a choice?
    simple_main()

    # Is the management of multiple agents working?
    agent_manager_main()

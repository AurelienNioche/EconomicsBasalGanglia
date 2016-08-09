import numpy as np
from collections import OrderedDict
from tqdm import tqdm
from multiprocessing import cpu_count
from module.eco import Economy
from module.save_eco import BackUp
from module.BGAgentsManager import BGAgentsManager
from module.RLAgentsManager import RLAgentsManager


class BGModelEconomy(Economy):

    def __init__(self, parameters):

        Economy.__init__(self, parameters=parameters)
        if parameters["model"] == "RL":
            self.agent_manager = RLAgentsManager(parameters=parameters)
        elif parameters["model"] == "BG":
            self.agent_manager = BGAgentsManager(parameters=parameters)
        else:
            raise Exception("Model '{}' is not implemented! Probably a typo in teh name of the model?"
                            .format(parameters["model"]))

        self.create_agents()

    def create_agents(self):

        self.agent_manager.create_agents()

    def have_agents_choose(self):

        self.choice[:] = self.agent_manager.have_agents_choose(self.decision)

        # Each vector component needs to be between 0 and 3 included
        self.i_choice[:] = (self.decision * 2) + self.choice

    def teach_agents(self):

        d_exchange = np.where((self.i_choice == 0) * (self.finding_a_partner == 1))[0]
        i_exchange = np.where((self.i_choice == 2) * (self.finding_a_partner == 1))[0]

        self.agent_manager.teach_agents(np.concatenate((d_exchange, i_exchange)))

    def quit(self):

        self.agent_manager.quit()


class SimulationRunner(object):

    def __init__(self, parameters):

        # Time the simulation should last
        self.t_max = parameters["t_max"]

        # Create the economy to simulate
        self.eco = BGModelEconomy(parameters)

    def run(self, single):

        # Run simulation for as time units as required.
        if single:
            for t in tqdm(range(self.t_max)):

                self.eco.run()
        else:

            for t in range(self.t_max):

                self.eco.run()

        self.eco.quit()

        return self.export()

    def export(self):

        data = OrderedDict(
            [
             ("indirect_exchanges", self.eco.indirect_exchanges),
             ("direct_exchanges", self.eco.direct_exchanges)
            ]
        )
        return data


class Launcher(object):

    @classmethod
    def launch(cls, parameters, single=True):

        ##################################
        #   Beginning of the program     #
        ##################################

        # Create a "simulation runner" that will manage the simulation.
        simulation_runner = SimulationRunner(parameters)

        # Ask the "simulation runner" to launch the simulation.
        return simulation_runner.run(single)

        ############################
        #   End of the program     #
        ############################


def simple_run():

    t_max = 500
    model = "BG"

    param = \
        {
            "workforce": np.array([50, 50, 100], dtype=int),
            "t_max": t_max,  # Set the number of time units the simulation will run.
            "cpu_count": cpu_count(),
            "model": model,
            "date": "example",
            "idx": 0
        }

    results = Launcher.launch(param)
    BackUp.save_data(results=results, parameters=param, root_folder="../../data")


if __name__ == "__main__":

    simple_run()

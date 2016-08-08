import numpy as np

############################################
#           NOTATION                       #
############################################

# For the needs of coding, we don't use systematically here the same notation as in the article.
# Here are the matches:

# For an object:
# 'i' means a production good;
# 'j' means a consumption good;
# 'k' means the third good.

# For agent type:
# * '0' means a type-12 agent;
# * '1' means a type-22 agent;
# * '2' means a type-31 agent.

# For a decision:
# * '0' means 'type-i decision';
# * '1' means 'type-k decision'.

# For a choice:
# * '0' means 'ij' if the agent faces a type-i decision and 'kj' if the agent faces a type-k decision;
# * '1' means 'ik'  if the agent faces a type-i decision and 'ki'  if the agent faces type-k decision.

# For markets,
# * '0' means the part of the market '12' where are the agents willing
#       to exchange type-1 good against type-2 good;
# * '1' means the part of the market '12' where are the agents willing
#       to exchange type-2 good against type-1 good;
# * '2' means the part of the market '23' where are the agents willing
#       to exchange type-2 good against type-3 good;
# * '3' means the part of the market '23' where are the agents willing
#       to exchange type-3 good against type-2 good;
# * '4' means the part of the market '31' where are the agents willing
#       to exchange type-3 good against type-1 good;
# * '5' means the part of the market '31' where are the agents willing
#       to exchange type-1 good against type-3 good.


class Economy(object):

    def __init__(self, parameters):

        self.n = np.sum(parameters["workforce"])  # Total number of agents
        self.workforce = np.zeros(len(parameters["workforce"]), dtype=int)
        self.workforce[:] = parameters["workforce"]  # Number of agents by type

        self.type = np.zeros(self.n, dtype=int)

        self.type[:] = np.concatenate(([0, ]*self.workforce[0],
                                       [1, ]*self.workforce[1],
                                       [2, ]*self.workforce[2]))

        # Each agent possesses an index by which he can be identified.
        #  Here are the the indexes lists corresponding to each type of agent:

        self.idx0 = np.where(self.type == 0)[0]
        self.idx1 = np.where(self.type == 1)[0]
        self.idx2 = np.where(self.type == 2)[0]

        #  The "placement array" is a 3-D matrix (d1: type, d2: decision, d3: choice).
        #  Allow us to retrieve the market where is supposed to go an agent according to:
        #  * his type,
        #  * the decision he faced,
        #  * the choice he made.

        self.placement = np.array(
            [[[0, 5],
              [3, 4]],
             [[2, 1],
              [5, 0]],
             [[4, 3],
              [1, 2]]
            ])

        self.place = np.zeros(self.n, dtype=int)

        # The "decision array" is a 3D-matrix (d1: finding_a_partner, d2: decision, d3: choice).
        # Allow us to retrieve the decision faced by an agent at t according to
        #  * the fact that he succeeded in his exchange at t-1,
        #  * the decision he faced at t-1,
        #  * the choice he made at t-1.
        self.decision_array = np.array(
            [[[0, 0],
              [1, 1]],
             [[0, 1],
              [0, 0]]])

        self.decision = np.zeros(self.n, dtype=int)

        self.choice = np.zeros(self.n, dtype=int)

        self.finding_a_partner = np.zeros(self.n, dtype=int)

        self.i_choice = np.zeros(self.n, dtype=int)

        self.t = -1

        self.indirect_exchanges = np.zeros((parameters["t_max"], 3))
        self.direct_exchanges = np.zeros((parameters["t_max"], 3))

    def run(self):

        self.t += 1

        # Make agents updating the decision they are facing
        self.update_decision()

        # Have agents choose in which market each of them want to go
        self.have_agents_choose()

        # Move the agents where they are supposed to go
        self.who_is_where()

        # Realize the transactions in the different markets
        self.make_the_transactions()

        # Make agents learn about the success rates of each type of exchange
        self.teach_agents()

        # Make some stats for future analysis
        self.make_some_stats()

    def update_decision(self):

        # Set the decision each agent faces at time t, according to the fact he succeeded or not in his exchange at t-1,
        #  the decision he previously faced, and the choice he previously made.
        self.decision[:] = self.decision_array[self.finding_a_partner,
                                               self.decision,
                                               self.choice]

    def have_agents_choose(self):

        # Needs to be overwritten
        pass

    def who_is_where(self):

        # Place the agents according to their type, decision and choice
        self.place[:] = self.placement[self.type, self.decision, self.choice]

    def make_the_transactions(self):

        # Re-initialize the variable for succeeded exchanges
        self.finding_a_partner[:] = 0

        # Find the attendance of each part of the markets
        ipp0 = np.where(self.place == 0)[0]
        ipp1 = np.where(self.place == 1)[0]
        ipp2 = np.where(self.place == 2)[0]
        ipp3 = np.where(self.place == 3)[0]
        ipp4 = np.where(self.place == 4)[0]
        ipp5 = np.where(self.place == 5)[0]

        # Make as encounters as possible
        for ip0, ip1 in [(ipp0, ipp1), (ipp2, ipp3), (ipp4, ipp5)]:  # Consider the two parts of each market

            # If there is nobody in this particular market, do not do nothing.
            if len(ip0) == 0 or len(ip1) == 0:

                pass

            # If there is less agents in one part of the market than in the other:
            #  * agents in the less attended part get successful (that is they can proceed to an exchange);
            #  * among the agent present in the most attended part, randomly select as agents in that part of the market
            #      that there is on the other market: these selected agents can proceed to their exchange.
            elif len(ip0) < len(ip1):

                self.finding_a_partner[ip0] = 1
                np.random.shuffle(ip1)
                self.finding_a_partner[ip1[:len(ip0)]] = 1

            else:

                self.finding_a_partner[ip1] = 1
                np.random.shuffle(ip0)
                self.finding_a_partner[ip0[:len(ip1)]] = 1

    def teach_agents(self):

        # Needs to be overwritten
        pass

    def make_some_stats(self):

        for i, idx in enumerate([self.idx0, self.idx1, self.idx2]):  # 3 types of agents
            ind1 = self.i_choice[idx][:] == 1
            ind2 = self.i_choice[idx][:] == 2
            self.indirect_exchanges[self.t][i] = np.mean(ind1+ind2)

            dir = self.i_choice[idx][:] == 0
            self.direct_exchanges[self.t][i] = np.mean(dir)



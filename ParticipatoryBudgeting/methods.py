import pickle
import numpy as np

from ParticipatoryBudgeting.k_approval import k_approval

from typing import List 

Ballot = List[int]
Ballots = List[Ballot]


class K_Approval(object):
    def __init__(self, ballots: Ballots, costs: List[int], kappa: int, max_budget: int):
        self.ballots = ballots
        self.costs = costs
        self.kappa = kappa 
        self.max_budget = max_budget

    def __call__(self):
        return k_approval(self.ballots, self.costs, self.max_budget, self.kappa)


class Value_for_money(object):
    def __init__(self, num_agents: int, num_projects: int):
        self.num_agents = num_agents
        self.num_projects = num_projects
        self.ballots = np.zeros((num_agents, num_projects), dtype=np.int32)

    def set_ballot(self, agent: int, ballot: Ballot) -> None:
        assert agent < self.num_agents, 'Invalid agent id (must be <{}).'.format(self.num_agents)
        assert len(ballot) < self.num_projects, 'Invalid ballot given (cannot give >{} projects)'.format(self.num_projects)        
        self.ballots[agent, :len(ballot)] = np.array(ballot)
        
    ## The function calculate_winners recieve as input the budget available for all the projects and the cost for each
    ## After calculate the ratios, the output is an array where the projects are accepted (-1) or rejected (-2),
    ## the money that is not expend and the number of votes for each project.
    def calculate_winners (self,max_budget, cost_per_project):
        total_votes = np.zeros(self.num_projects)
        for agent in self.ballots:
            total_votes = np.sum([total_votes, agent], axis=0)
        ratio_per_project = np.true_divide(total_votes,cost_per_project)
        done = False
        while(done == False):
            maxElement = np.argmax(ratio_per_project)
            if (ratio_per_project[maxElement] < 0.0):
                done = True
            elif ((max_budget - cost_per_project[maxElement]) >= 0):
                max_budget = max_budget - cost_per_project[maxElement]
                ratio_per_project[maxElement] = -1
            else:
                ratio_per_project[maxElement] = -2
        return ratio_per_project, max_budget, total_votes


def example_with_k_approval():

    for i in range(10):
        ballots = np.load('./ParticipatoryBudgeting/ballots{}.npy'.format(i))
        costs = pickle.load(open('./costs_2017.p', "rb"))
        budget = 42e06
        K = 20

        # wrap everything into an object
        k_app = K_Approval(ballots=ballots, costs=costs, kappa=K, max_budget=budget)

        # just call to see the winning projects 
        winners, budget = k_app()

        print('SIMULATION {}'.format(i))
        print('-'*100)
        print(len(winners))

        winning_votes = 0
        winning_costs = 0
        total_votes = 0
        for j in range(len(winners)):
            winning_votes += sum(ballots[:,winners[j]])

        for k in range(ballots.shape[1]):
            total_votes += sum(ballots[:,k])

        print('avg satisf={}.'.format(float(winning_votes/total_votes))) 
        print('cost per winning vote={}'.format(float(budget/winning_votes)))
        print('-'*100)
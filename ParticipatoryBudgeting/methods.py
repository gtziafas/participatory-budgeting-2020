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

class Knapsack_Voting(object):
    def __init__(self, num_agents: int, num_projects: int):
        self.num_agents = num_agents
        self.num_projects = num_projects
        self.ballots = np.zeros((num_agents, num_projects), dtype=np.int32)
        self.knapsack = 0
        
    def set_ballot(self, agent: int, ballot: Ballot) -> None:
        assert agent < self.num_agents, 'Invalid agent id (must be <{}).'.format(self.num_agents)
        assert len(ballot) < self.num_projects, 'Invalid ballot given (cannot give >{} projects)'.format(self.num_projects)        
        self.ballots[agent, :len(ballot)] = np.array(ballot)
    def calculate_winners(self,ballot,max_budget, cost_per_project):
        approval_votes = [0 for x in range(self.num_projects)]
        for i in range(self.num_agents):
            a = np.where(ballot[i]==1)[0]
            for j in a:
                approval_votes[j] += 1
        knapsack = []
        for i in range(len(approval_votes)):
            knapsack.append([i,approval_votes[i]])
        knapsack.sort(key = lambda x: x[1]) 
        knapsack = knapsack[::-1]
        budget_pool = 0
        winners = []
        i = 0
        while budget_pool < max_budget:
            if budget_pool + cost_per_project[knapsack[i][0]] > max_budget:
                break
            budget_pool += cost_per_project[knapsack[i][0]]
            winners.append(knapsack[i][0])
            i += 1
        self.knapsack = knapsack
        self.winners = winners
        self.budget_pool = budget_pool
        return winners,budget_pool,knapsack
    def results():
        average_satisfaction = sum(n for _, n in self.knapsack[:len(self.winners)])/sum(n for _, n in self.knapsack)
        vote_per_dollar = sum(n for _, n in self.knapsack[:len(self.winners)])/self.budget_pool
        
        return vote_per_dollar,average_satisfaction
                              
    
    
    
def example_with_k_approval():
    ballots = np.load('./ParticipatoryBudgeting/ballots0.npy')
    costs = pickle.load(open('./costs_2017.p', "rb"))
    budget = 42e06
    K = 20

    # wrap everything into an object
    k_app = K_Approval(ballots=ballots, costs=costs, kappa=K, max_budget=budget)

    # just call to see the winning projects 
    k_app()

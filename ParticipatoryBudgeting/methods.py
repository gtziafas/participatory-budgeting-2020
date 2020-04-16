import numpy as np 

from ParticipatoryBudgeting.data import *

from typing import List 

Ballot = List[int]

class K_approval(object):
    def __init__(self, num_agents: int, num_projects: int):
        self.num_agents = num_agents
        self.num_projects = num_projects
        self.ballots = np.zeros((num_agents, num_projects), dtype=np.int32)

    def set_ballot(self, agent: int, ballot: Ballot) -> None:
        assert agent < self.num_agents, 'Invalid agent id (must be <{}).'.format(self.num_agents)
        assert len(ballot) < self.num_projects, 'Invalid ballot given (cannot give >{} projects)'.format(self.num_projects)        
        self.ballots[agent, :len(ballot)] = np.array(ballot)
        
class Value_for_money(object):
    def __init__(self, num_agents: int, num_projects: int):
        self.num_agents = num_agents
        self.num_projects = num_projects
        self.ballots = np.zeros((num_agents, num_projects), dtype=np.int32)

    def set_ballot(self, agent: int, ballot: Ballot) -> None:
        assert agent < self.num_agents, 'Invalid agent id (must be <{}).'.format(self.num_agents)
        assert len(ballot) < self.num_projects, 'Invalid ballot given (cannot give >{} projects)'.format(self.num_projects)        
        self.ballots[agent, :len(ballot)] = np.array(ballot)
        
    def calculate_winners (self,max_budget, cost_per_project):
        total_votes = np.zeros(self.num_projects)
        for agent in ballot:
            total_votes = np.sum([total_votes, self.ballots], axis=0)
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

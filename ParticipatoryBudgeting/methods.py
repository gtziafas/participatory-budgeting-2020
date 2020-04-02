import numpy as np 

from KnapshackNewYork.data import *

Ballot = List[int]

class K_approval(object):
    def __init__(self, num_agents: int, num_projects: int):
        self.num_agents = num_agents
        self.num_projects = num_projects
        self.ballots = np.zeros((num_agents, num_projects), dtype=np.int32)

    def set_ballot(self, agent: int, ballot: Ballot) -> None:
        assert agent < self.num_agents, 'Invalid agent id (must be <{}).'.format(self.num_agents)
        assert len(ballot) < self.num_projects, 'Invalid ballot given (cannot give >{} projects'.format(self.num_projects)        
        self.ballots[agent, :len(ballot)] = np.array(ballot)

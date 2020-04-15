import pandas as pd 
import numpy as np

from typing import Tuple, List, Optional

Sample = Tuple[int, str, str, int, str, str, str, int, bool, int]
Samples = List[Sample]
Ballot = [np.int32]
Ballots = [Ballot]


def normalize_votes(votes: List[str]) -> List[int]:
    return list(map(int, list(map(np.nan_to_num, votes))))


def get_votes_from_listed(listed: Samples) -> List[int]:
    return normalize_votes(list(map(lambda l: l[7], listed)))


class ParticipatoryBudgetingDataset(object):
    def __init__(self, csv_file: str) -> None:
        self.csv = pd.read_csv(csv_file)
        self.set_cols()

    def set_cols(self) -> None:
        self.listed = self.csv.values.tolist()
        self.vote_years = list(map(lambda l: l[0], self.listed))
        self.council_districts = list(map(lambda l: l[1], self.listed))
        self.categories = list(map(lambda l: l[2], self.listed))
        self.project_numbers = list(map(lambda l: l[3], self.listed))
        self.titles = list(map(lambda l: l[4], self.listed))
        self.descriptions = list(map(lambda l: l[5], self.listed))
        self.addresses = list(map(lambda l: l[6], self.listed))
        self.votes = normalize_votes(list(map(lambda l: l[7], self.listed)))
        self.winners = list(map(lambda l: l[8], self.listed))
        self.costs = list(map(lambda l: l[9], self.listed))


    def __len__(self) -> int:
        return len(self.listed)

    def __getitem__(self, i: int) -> Sample:
        year, distr, cat, num, title, descr, address, votes, winner, cost = self.listed[i][:10]
        return year, distr, cat, num, title, descr, address, votes, winner, cost

    def filter_year(self, year: int) -> Samples:
        return list(filter(lambda l: l[0] == year, self.listed))

    def filter_winners(self) -> Samples:
        return list(filter(lambda l: l[8], self.listed))

    def filter_cost(self, cost_thresh: int, upper: Optional[bool]=True) -> Samples:
        if not upper:
            return list(filter(lambda l: l[9] > cost_thresh, self.listed))
        return list(filter(lambda l: l[9] < cost_thresh, self.listed))

    def filter_votes(self, votes_thresh: int, upper: Optional[bool]=True) -> Samples:
        if not upper:
            return list(filter(lambda l: l[9] > votes_thresh, self.listed))
        return list(filter(lambda l: l[7] < votes_thresh, self.listed))


def generate_random_ballots(dataset: Samples, votes: List[int], num_voters: int) -> Ballots:
    num_projects = len(dataset)
    ballots = np.zeros((num_voters, num_projects), dtype=np.int32)

    for i in range(len(votes)):
        temp = np.zeros(num_voters, dtype=np.int32)
        temp[:votes[i]] = 1
        np.random.shuffle(temp)
        ballots[:, i] = temp

    return ballots


def pbnyc_ballots():
    dataset = ParticipatoryBudgetingDataset('Participatory_Budgeting_Projects.csv')
    num_voters = 65000
    num_simulations = 10 
    year = 2017

    data = dataset.filter_year(year)
    votes = get_votes_from_listed(data)

    for s in range(num_simulations):
        ballots = generate_random_ballots(data, votes, num_voters)
        np.save('pbnyc_ballots_2017_{}.npy'.format(s), ballots)
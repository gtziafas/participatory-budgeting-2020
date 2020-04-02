import pandas pd 

from typing import Tuple, List

Sample = Tuple[int, str, str, int, str, str, str, int, bool, int]
Samples = List[Sample]

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
        self.votes = list(map(lambda l: l[7], self.listed))
        self.winners = list(map(lambda l: l[8], self.listed))
        self.costs = list(map(lambda l: l[9], self.listed))


    def __len__(self) -> int:
        return len(self.listed)

    def __getitem__(self, i: int) -> Sample:
        year, distr, cat, num, title, descr, address, votes, winner, cost = *self.listed[i]
        return eval(year), distr, cat, eval(num), title, descr, address, eval(votes), bool(winner), eval(cost)

    def filter_year(self, year: int) -> Samples:
        return list(filter(lambda l: l[0] == year, self.listed))

    
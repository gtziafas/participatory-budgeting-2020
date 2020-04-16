import random
import pickle
import numpy as np 

from collections import OrderedDict
from typing import List 

Ballot = [np.int32]
Ballots = [Ballot]


def filter_k_votes(ballots: Ballots, kappa: int) -> Ballots:
    num_voters, num_projects = ballots.shape
    filtered_ballots = np.zeros_like(ballots)

    # find which projects are selected by each voter
    idces = list(map(lambda i: np.where(ballots[i]==1)[0], list(range(num_voters))))

    # sample at most K of them
    choices = list(map(lambda idx: random.choices(idx, k=kappa), idces))

    # return the new ballots
    for i in range(num_voters):
        filtered_ballots[i, choices[i]] = 1

    return filtered_ballots


def rank_projects(ballots: Ballots) -> List[int]:
    num_voters, num_projects = ballots.shape

    # get the votes for each project
    votes = list(map(lambda i: sum(ballots[:,i]), list(range(num_projects))))

    # sort in descending order 
    votes_sorted = sorted(votes, reverse=True)
    ranked = list(map(lambda v: votes_sorted.index(v), votes))

    # remove duplicates
    ranked = list(OrderedDict.fromkeys(ranked))

    return ranked


def decide_winners(projects: List[int], costs: List[int], max_budget: int) -> List[int]:
    # assuming projects ranked by voter's selections
    current_budget, idx = 0, 0
    winners = []
    while current_budget <= max_budget:
        winners.append(projects[idx])
        current_budget += costs[projects[idx]]
        idx += 1
    return winners


def k_approval(ballots: Ballots, costs: List[int], max_budget: int, kappa: int) -> List[int]:

    # sample at most K projects per voter
    ballots = filter_k_votes(ballots, kappa)

    # rank them according to the votes
    ranked_projects = rank_projects(ballots)

    # decide the winner
    winners = decide_winners(ranked_projects, costs, max_budget)

    return winners


def main(ballots_filepath: str, costs_picklefile: str):
    ballots = np.load(ballots_filepath)
    costs = pickle.load(open(costs_picklefile, "rb"))
    max_budget = 42e06

    kappas = [10, 20, 50, 100]
    winners = []
    for k in kappas:
        winner = k_approval(ballots, costs, max_budget, k)
        winners.append(winner)
        print('For {}-approval, winners are:\n{}'.format(k, winner))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--ballots_filepath', help='where to load the ballots matrix from', type=str)
    parser.add_argument('-c', '--costs_picklefile', help='where to load the cost for each project from (picle format)', type=str)

    kwargs = vars(parser.parse_args())
    main(**kwargs)





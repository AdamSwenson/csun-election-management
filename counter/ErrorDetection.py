"""
Tools for detecting problems with lists of candidates
Created by adam on 3/11/19
"""
__author__ = 'adam'

from counter.Exceptions import VoteStuffingError


def check_vote_stuffing(rowId, list_of_selections):
    if len(list_of_selections) > len(set(list_of_selections)):
        raise VoteStuffingError(rowId, list_of_selections)


if __name__ == '__main__':
    pass
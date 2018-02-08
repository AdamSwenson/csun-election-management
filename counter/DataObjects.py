"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

from collections import namedtuple
# OfficeElection = namedtuple('OfficeElection', ['officeName', 'fieldName', 'candidateNames', 'maxValid'])


class OfficeElection(object):
    def __init__(self, officeName, fieldName, candidateNames, maxValid):
        self.officeName = officeName
        self.maxValid =maxValid
        self.fieldName = fieldName
        self.candidateNames = candidateNames

if __name__ == '__main__':
    pass
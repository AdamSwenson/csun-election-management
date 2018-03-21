"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

# from collections import namedtuple
# OfficeElection = namedtuple('OfficeElection', ['officeName', 'fieldName', 'candidateNames', 'maxValid'])


class OfficeElection(object):
    """
    This defines the properties of a contest for a single office.
    The typical faculty election cycle is defined as a list of several of these objects
    """

    def __init__(self, officeName, fieldName, candidateNames, maxValid):
        """
        :param officeName: The name of the position being contested
        :param fieldName: The string in the header row of the results by which we identify the office
        :param candidateNames: A list of strings. These should be candidate names as appear in the results.
        :param maxValid: The maximum number of candidates a voter may select for the office.
        """
        self.officeName = officeName
        self.maxValid = maxValid
        self.fieldName = fieldName
        self.candidateNames = candidateNames


if __name__ == '__main__':
    pass
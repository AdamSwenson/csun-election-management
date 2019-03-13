"""
Created by adam on 2/5/18
"""
from counter.Exceptions import InvalidatesVote
import pandas as pd

__author__ = 'adam'

# from collections import namedtuple
# OfficeElection = namedtuple('OfficeElection', ['officeName', 'fieldName', 'candidateNames', 'maxValid'])


class OfficeElection(object):
    """
    This defines the properties of a contest for a single office.
    The typical faculty election cycle is defined as a list of several of these objects
    """

    def __init__(self, officeName=None, fieldName=None, writeInFieldNames=[], candidateNames=[], maxValid=None):
        """
        :param officeName: The name of the position being contested
        :param fieldName: The string in the header row of the results by which we identify the office
        :param candidateNames: A list of strings. These should be candidate names as appear in the results.
        :param maxValid: The maximum number of candidates a voter may select for the office.
        """
        self.errors = []
        self.office_votes = []
        self.possible_errors = []

        self.writeInFieldNames = writeInFieldNames
        self.officeName = officeName
        self.maxValid = maxValid
        self.fieldName = fieldName
        self.candidateNames = candidateNames

    def add_data( self, frame ):
        """Takes the dataframe and stores the relevant rows
        """
        self.data = frame[self.office_columns]

    def add_error( self , error):
        self.errors.append(error)

    def add_selected_candidates( self, candidate_list ):
        """Series or other object with candidate names
        as keys and vote counts as values"""
        self.office_votes += candidate_list

    @property
    def number_abstentions( self ):
        return len(self.data) - len(self.data.dropna(how='all'))

    @property
    def total_voters( self ):
        """The row count for the office.
        This includes invalid votes and abstentions"""
        return len(self.data)

    @property
    def invalid_votes( self ):
        if len(self.errors) == 0:
            return 0
        return len(self.invalid_rows)

    @property
    def invalid_rows( self ):
        """Returns the row ids of invalid votes"""
        return [e.rowId for e in self.errors if isinstance(e, InvalidatesVote)]

    @property
    def office_columns( self ):
        return [ self.fieldName ] + self.writeInFieldNames

    @property
    def votes( self ):
        return self.total_votes - self.invalid_votes

    @property
    def vote_counts( self ):
        office_votes = pd.Series( self.office_votes, name='number_votes' )
        return office_votes.value_counts()

    @property
    def writeinFieldName(self):
        """Only used in canvas election"""
        return "%s-writein" % self.fieldName

if __name__ == '__main__':
    pass
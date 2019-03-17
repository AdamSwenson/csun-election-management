"""
Created by adam on 2/5/18
"""
import pandas as pd

from counter.Exceptions import InvalidatesVote, VoteStuffingError

__author__ = 'adam'


# from collections import namedtuple
# OfficeElection = namedtuple('OfficeElection', ['officeName', 'fieldName', 'candidateNames', 'maxValid'])


class OfficeElection( object ):
    """
    This defines the properties of a contest for a single office.
    The typical faculty election cycle is defined as a list of several of these objects
    """

    def __init__( self, officeName=None, fieldName=None, writeInFieldNames=[ ], candidateNames=[ ], maxValid=None, requires_majority=False ):
        """
        :param officeName: The name of the position being contested
        :param fieldName: The string in the header row of the results by which we identify the office
        :param candidateNames: A list of strings. These should be candidate names as appear in the results.
        :param maxValid: The maximum number of candidates a voter may select for the office.
        """
        self.requires_majority = requires_majority
        self.errors = [ ]
        self.office_votes = [ ]
        self.possible_errors = [ ]

        self.writeInFieldNames = writeInFieldNames
        self.officeName = officeName
        self.maxValid = maxValid
        self.fieldName = fieldName
        self.candidateNames = candidateNames

    def add_data( self, frame ):
        """Takes the dataframe and stores the relevant rows
        """
        self.data = frame[ self.office_columns ]

    def add_error( self, error ):
        self.errors.append( error )

    def add_selected_candidates( self, candidate_list ):
        """Series or other object with candidate names
        as keys and vote counts as values"""
        self.office_votes += candidate_list

    @property
    def cast_votes( self ):
        """The row count for the office.
        This includes illegal votes and abstentions
            Cast = abstentions + legal + illegal
        Cast votes plays no role except for auditing
        """
        return len( self.data )

    @property
    def combined_results_frame( self ):
        """Returns a dataframe which combines the vote counts and pcts of
        valid votes"""
        return pd.DataFrame([self.vote_counts, self.percentages_of_valid])

    @property
    def number_abstentions( self ):
        """The count of blank ballots for the office"""
        return len( self.data ) - len( self.data.dropna( how='all' ) )

    @property
    def illegal_votes( self ):
        """
        Illegal: The ballot expresses a preference which cannot be satisfied
        within the bounds of the election. This can include:
            - The voter selecting more than the allowed number of candidates; or,
            - Selecting the maximum number and then writing in an additional
            candidate.
        """
        if len( self.errors ) == 0:
            return 0
        return len( self.illegal_rows )

    @property
    def percentages_of_valid( self ):
        """Returns the percentage each candidate received of the total
        valid votes"""
        s = self.vote_counts.apply(lambda x: (x / self.valid_votes)*100)
        s.name = 'pct_of_valid'
        return s

    @property
    def illegal_rows( self ):
        """Returns the row ids of illegal_votes"""
        return [ e.rowId for e in self.errors if isinstance( e, InvalidatesVote ) or isinstance(e, VoteStuffingError) ]

    @property
    def office_columns( self ):
        return [ self.fieldName ] + self.writeInFieldNames

    @property
    def valid_votes( self ):
        """
        Returns the count of legal and illegal valid_votes cast,
        less the abstentions
            valid = legal + illegal
        These determine the denominator when a position requires
        a majority (i.e., > 50%)
        """
        return self.cast_votes - self.number_abstentions

    @property
    def vote_counts( self ):
        office_votes = pd.Series( self.office_votes, name='number_votes' )
        return office_votes.value_counts()

    @property
    def writeinFieldName( self ):
        """Only used in canvas election"""
        return "%s-writein" % self.fieldName


if __name__ == '__main__':
    pass

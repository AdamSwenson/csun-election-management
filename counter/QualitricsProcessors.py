"""
These are tools for dealing with results files
from elections conducted via Qualitrics

Created by adam on 3/11/19
"""
from counter.DataObjects import OfficeElection

__author__ = 'adam'

from counter.QualitricsHelpers import is_placeholder

import pandas as pd
import counter.environment as env
from counter.Exceptions import VoteStuffingError, OfficeProcessingError
from counter.ErrorDetection import check_vote_stuffing
from counter.Loggers import WriteInVoteLogger
from counter.StringProcessors import remove_depts


def process_field( field, keep_depts=False ):
    """Extracts all votes from a given cell"""
    if not keep_depts:
        field = remove_depts( field )
    votes = field.split( ',' )
    # clean up whitespace
    votes = [ v.strip() for v in votes if not is_placeholder( v ) ]
    return votes


def process_voter( rowId: int, row, main_column: str, write_in_columns: list ):
    """Process all the fields for an individual voter
    :param rowId:
    :param row: A DataFrame row representing one voter
    :param main_column: The name of the non-write-in vote column
    :param write_in_columns: List containing the names of write-in columns
    :return: list containing all names that were voted for
    """
    votes = [ ]
    write_in_votes = False
    # process the main vote column
    votes += process_field( row[ main_column ] )
    # process the write ins
    for column in write_in_columns:
        if not pd.isnull( row[ column ] ):
            votes.append( row[ column ] )
            write_in_votes = True
    # Checks for illegal votes go here

    if write_in_votes:
        # Log the write in voted
        env.writeInLogger.log( main_column, rowId, votes )
        check_vote_stuffing( rowId, votes )

    return votes


def process_office_columns( frame: pd.DataFrame, results: OfficeElection):
    """
    main_column: String label of the main vote column (e.g., 'Q1')
    """
    office_columns = results.office_columns #[ main_column ] + write_in_columns
    office_votes = [ ]
    # We don't keep these in the results object because they don't affect
    # the vote count. They mean we don't really have a count yet
    possible_errors = []

    # for idx, row in frame[ office_columns ].iterrows():
    for idx, row in results.data.iterrows():
        try:
            office_votes += process_voter( idx, row, results.fieldName, results.writeInFieldNames )
            results.add_selected_candidates(office_votes)
        # We want to catch all possible errors on the first run so
        # that the operator isn't stuck fixing an error, running the counter
        # and fixing another, ad infinitum.
        # Thus we'll capture any errors and hang on to them so that
        # we can report them instead of returning counts
        except VoteStuffingError as e:
            possible_errors.append(e)

    # Check whether there are any errors and abort
    # reporting if there are
    if len(possible_errors) > 0:
        raise OfficeProcessingError(possible_errors)

    return results.vote_counts

    # # Make votes into a series and count it
    # office_votes = pd.Series( office_votes, name='number_votes' )
    # return office_votes.value_counts()


if __name__ == '__main__':
    pass

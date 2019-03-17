"""
These are tools for dealing with results files
from elections conducted via Qualitrics

Created by adam on 3/11/19
"""
from counter.DataObjects import OfficeElection
from counter.Definitions import OfficeDefinitions

__author__ = 'adam'

from counter.QualitricsHelpers import is_placeholder, get_results_column_names, get_write_in_column_names

import pandas as pd
import counter.environment as env
from counter.Exceptions import VoteStuffingError, OfficeProcessingError
from counter.ErrorDetection import check_vote_stuffing
from counter.Loggers import WriteInVoteLogger
from counter.StringProcessors import remove_depts


def process_field( field, keep_depts=False ):
    """Extracts all valid_votes from a given cell"""
    # if type(field) != str:
    #     return field
    #
    if not keep_depts:
        field = remove_depts( field )
    try:
        votes = field.split( ',' )
        # clean up whitespace
        votes = [ v.strip() for v in votes if not is_placeholder( v ) ]
        return votes
    except Exception as e:
        print(e)


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
    try:
        # process the main vote column
        if not pd.isnull( row[ main_column ] ):
            votes += process_field( row[ main_column ] )
        # process the write ins
        for column in write_in_columns:
            if not pd.isnull( row[ column ] ):
                votes.append( row[ column ] )
                write_in_votes = True
        # Checks for illegal valid_votes go here
    except Exception as e:
        print(rowId, main_column, write_in_columns, row[main_column], row[write_in_columns])
    if write_in_votes:
        # Log the write in voted
        env.writeInLogger.log( main_column, rowId, votes )
        check_vote_stuffing( rowId, votes )

    return votes


def process_office_columns( results: OfficeElection):
    """
    main_column: String label of the main vote column (e.g., 'Q1')
    """

    # We don't keep these in the results object because they don't affect
    # the vote count. They mean we don't really have a count yet
    possible_errors = []

    # for idx, row in frame[ office_columns ].iterrows():
    for idx, row in results.data.iterrows():
        try:
            office_votes = process_voter( idx, row, results.fieldName, results.writeInFieldNames )
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


def process_results(frame, definition_filepath, election):
    """This is the master processing function
    Returns a list of results objects for each office where no errors
    were encountered.
    """
    # Read in the properties of the various offices
    Definitions = OfficeDefinitions(definition_filepath, election)
    results = []

    results_columns = get_results_column_names(frame)
    for c in results_columns:
        # create a data store object
        office_name = Definitions.get_office_name_for_field(c)
        requires_maj = Definitions.office_requires_majority(c)
        write_in_columns = get_write_in_column_names(frame, c)
        r = OfficeElection(officeName=office_name,
                           fieldName=c,
                           writeInFieldNames=write_in_columns,
                           requires_majority=requires_maj
                           )
        # The result object will pull out the relevant columns
        r.add_data(frame)
        try:
            # This saves the results back into the result object
            process_office_columns(r)
            results.append(r)
        except OfficeProcessingError as err:
            # These blocked the results object from being added to the
            # results list
            print("Error proccessing office: {}".format(office_name))
            for e in err.errors:
                print(e)
    return results


def save_results(output_file, results):
    """Writes results to output file"""
    with pd.ExcelWriter(output_file) as writer:
        for result in results:
            #             print("Writing results of {} to file".format(result.officeName))
            result.vote_counts.to_excel(writer, sheet_name=result.officeName)


if __name__ == '__main__':
    pass

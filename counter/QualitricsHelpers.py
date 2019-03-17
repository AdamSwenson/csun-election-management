"""
Created by adam on 3/12/19
"""
__author__ = 'adam'

import pandas as pd


def get_results_column_names( frame ):
    """Since we don't know how many questions there
    will be, this returns all columns with the format
    Qx where x is an integer"""
    results_columns = [ ]
    i = 1

    try:
        while True:
            c = 'Q{}'.format( i )
            if c in frame.columns:
                results_columns.append( c )
                i += 1
            else:
                raise StopIteration
    except StopIteration:
        return results_columns


def get_write_in_column_names( frame, question_number ):
    """Write in columns seem to have the format
    'Q1_5_TEXT', 'Q1_6_TEXT'
    Thus this finds the relevant write in columns for a
    given question
    """
    if type( question_number ) is int:
        question_number = 'Q{}'.format( question_number )
    write_in_columns = [ ]
    for col in frame.columns:
        s = col.split( '_' )
        # Write ins will have 3 items
        if len( s ) > 1:
            if s[ 0 ] == question_number:  # and s[-1] == 'TEXT':
                write_in_columns.append( col )
    return write_in_columns


def is_placeholder( candidate ):
    return candidate.strip().lower()[ :5 ] == 'write'
    # return candidate.strip().lower()[ :20 ] == 'write-in candidate #'


def load_and_prepare( results_file ):
    data = pd.read_csv( results_file )
    # Remove non-response rows
    dropped = data[ data.index <= 1 ]
    data = data[ data.index > 1 ]
    # remove unneeded columns
    drop_columns = [ 'DistributionChannel', 'UserLanguage', 'Status' ]
    data.drop( drop_columns, axis=1, inplace=True )
    data.dropna( how='all', axis=0, inplace=True )
    # format timestamps
    date_fields = [ 'StartDate', 'EndDate', 'RecordedDate' ]

    def make_ts( row ):
        return pd.to_datetime( row[ date_fields ] )

    data[ date_fields ] = data.apply( lambda x: make_ts( x ), axis=1 )
    return data

"""
Created by adam on 3/15/19
"""
import pandas as pd

# from ProcessorsTests import fake
# from test_officeElection import fake

__author__ = 'adam'


from faker import Faker
from pandas import DataFrame

import counter.DataObjects as DO
import counter.Processors as P

fake = Faker()

NUMBER_VOTERS = 3
NUMBER_CANDIDATES = 3
NUMBER_INVALID = 0

FIELD_NAME = fake.bs()
OFFICE_NAME = fake.bs()


def make_test_data( col_names, num_votes, num_abstentions, num_per_office=1 ):
    f = [ ]
    for i in range( 0, num_votes - num_abstentions ):
        if num_per_office == 1:
            f.append( { n: make_candidate() for n in col_names } )
        else:
            f.append( { n: make_multiple_candidate_cell(num_per_office) for n in col_names } )
    for j in range( 0, num_abstentions ):
        f.append( { n: None for n in col_names } )
    return pd.DataFrame( f )


def make_candidate():
    dept = "%s %s %s" % (fake.word(), fake.word(), fake.word())
    return "%s %s (%s)" % (fake.first_name(), fake.last_name(), dept)


def make_multiple_candidate_cell(num_per_cell=2):
    return [ "{},".format(make_candidate()) for i in range(0, num_per_cell)]
    # dept = "%s %s %s" % (fake.word(), fake.word(), fake.word())
    # n =  "%s %s (%s)" % (fake.first_name(), fake.last_name(), dept)


if __name__ == '__main__':
    pass

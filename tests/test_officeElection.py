"""
Created by adam on 3/14/19
"""
from tests.DummyDataTools import make_test_data

__author__ = 'adam'

# # import counter.environment
# TEST_PATH = os.path.abspath( os.path.dirname( __file__ ) )
# # Folders outside of the project foler
# enclosing = os.path.abspath( os.path.dirname( TEST_PATH ) )
# sys.path.append( TEST_PATH )
# # sys.path.append(enclosing)
# sys.path.append( "%s/counter" % enclosing )
# # print(PROJ_PATH)
# print( enclosing )

import unittest
from unittest import TestCase
from counter.DataObjects import OfficeElection
from counter.Exceptions import VoteStuffingError

from faker import Faker

fake = Faker()


class OfficeElectionTests( TestCase ):
    def setUp( self ):
        pass

    def test_number_abstentions( self ):
        office_name = [ 'office1' ]
        num_abstentions = 5
        obj = OfficeElection( officeName=office_name[ 0 ] )
        d = make_test_data( office_name, 10, num_abstentions )
        obj.data = d
        # check
        self.assertEqual( obj.number_abstentions, num_abstentions )

    def test_cast_votes( self ):
        """The row count for the office.
        This includes illegal votes and abstentions
            Cast = abstentions + legal + illegal
        Cast votes plays no role except for auditing
        """
        # num_illegal = 6
        num_abstentions = 5
        num_legal = 7

        obj = OfficeElection(  )
        d = make_test_data( fake.text(), num_legal, num_abstentions )
        obj.data = d

        # check
        # todo Need to include illegal rows?
        self.assertEqual( len(obj.data), num_abstentions + num_legal )

    def test_illegal_votes( self ):
        """Illegal: The ballot expresses a preference which cannot be satisfied
        within the bounds of the election. This can include:
            - The voter selecting more than the allowed number of candidates; or,
            - Selecting the maximum number and then writing in an additional
            candidate.        """
        num_illegal = 5
        obj = OfficeElection()
        obj.errors = [ VoteStuffingError( i, [ fake.name(), fake.name() ] ) for i in range( 0, num_illegal ) ]
        self.assertEqual(num_illegal, obj.illegal_votes)

    def test_illegal_rows( self ):
        """Returns the row ids of illegal_votes"""
        num_illegal = 5
        obj = OfficeElection()
        obj.errors = [ VoteStuffingError( i, [ fake.name(), fake.name() ] ) for i in range( 0, num_illegal ) ]
        for i in range(0, num_illegal):
            self.assertIn(i, obj.illegal_rows)

    def test_office_columns( self ):
        self.fail()

    def test_valid_votes( self ):
        """
        Returns the count of legal and illegal valid_votes cast,
        less the abstentions
            valid = legal + illegal
        These determine the denominator when a position requires
        a majority (i.e., > 50%)
        todo: Make sure that this doesn't overcount write-ins where there is the 'WRITE IN #1" entries
        """
        num_illegal = 6
        num_abstentions = 5
        num_legal = 7
        obj = OfficeElection()
        obj.possible_errors = [ VoteStuffingError( i, [ fake.name(), fake.name() ] ) for i in range( 0, num_illegal ) ]

        obj = OfficeElection(  )
        d = make_test_data( fake.text(), num_legal, num_abstentions )
        obj.data = d
        # check
        self.assertEqual( obj.valid_votes, num_illegal + num_legal )

    def test_vote_counts( self ):
            self.fail()


if __name__ == '__main__':
    unittest.main()

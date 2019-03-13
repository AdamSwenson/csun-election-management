"""
Created by adam on 3/11/19
"""
from unittest import TestCase
from counter.QualitricsProcessors import process_field
from counter.QualitricsHelpers import get_results_column_names, get_write_in_column_names
from pandas import DataFrame

__author__ = 'adam'

test_cases =[
    (
        "Idris Elba (Age 46),Dwayne Johnson (Age 48)",
        ['Idris Elba', 'Dwayne Johnson']
    ),
    (
        "Idris Elba (Family, science, and consumers ),Dwayne Johnson ( Geology)",
        ['Idris Elba', 'Dwayne Johnson']
    ),
    (
        "Idris Elba (Family, science, and consumers ) ,Dwayne Johnson(Geology)",
        ['Idris Elba', 'Dwayne Johnson']
    ),

    (
        "Idris Elba(Family, science, and consumers),Dwayne Johnson(Geology) ",
        ['Idris Elba', 'Dwayne Johnson']
    )

]

def make_test_frame(maxval=4):
    test_frame = { }
    expected = []
    for i in range(1, maxval + 1):
        e = []
        qnum = 'Q{}'.format(i)
        for j in range(1, maxval + 1):
            # add the main column
            test_frame[qnum] = [i,  qnum]
            c = 'Q{}_{}_TEXT'.format(i, j)
            # add the write in column
            test_frame[c] = [i,  qnum]
            e.append(c)
        expected.append((i, qnum, e))

    test_frame = DataFrame(test_frame)
    return {'test_frame': test_frame, 'expected': expected}


class TestGet_write_in_columns( TestCase ):
    def test_get_write_in_columns( self ):
        r = make_test_frame()

        for exp in r['expected']:
            found_columns = get_write_in_column_names( r[ 'test_frame' ], exp[0 ] )
            for c in found_columns:
                self.assertIn(c,  exp[2])


class TestGet_results_columns( TestCase ):
    def test_get_results_columns( self ):
        self.fail()


class TestProcess_field( TestCase ):
    def test_process_field( self ):
        for raw, expected in test_cases:
            self.assertEqual(process_field(raw), expected)


if __name__ == '__main__':
    pass


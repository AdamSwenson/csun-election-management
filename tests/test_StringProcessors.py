"""
Created by adam on 3/11/19
"""
__author__ = 'adam'

from unittest import TestCase
from counter.StringProcessors import find_dept, remove_depts


class TestRemove_depts( TestCase ):
    def test_remove_depts( self ):
        test_field = "Idris Elba (Age 46),Dwayne Johnson (Age 48)"
        expected = 'Idris Elba ,Dwayne Johnson '
        self.assertEqual(remove_depts(test_field), expected)


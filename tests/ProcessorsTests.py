import unittest

from faker import Faker
from pandas import DataFrame

import counter.DataObjects as DO
import counter.Processors as P
from DummyDataTools import make_candidate

fake = Faker()

NUMBER_VOTERS = 3
NUMBER_CANDIDATES = 3
NUMBER_INVALID = 0

FIELD_NAME = fake.bs()
OFFICE_NAME = fake.bs()


def make_initialized_results(candidates):
    expected = {'invalid': 0}
    for c in candidates:
        expected[c] = 0
    return expected


def make_vote_string(candidates):
    """Creates the record we are expecting to find in the canvas export"""
    if type(candidates) is str:
        candidates = [candidates]
    r = ""
    for c in candidates:
        r = "%s,%s" % (r, c)
    # slice before return to remove an initial comma
    return r[1:]


class VoteCounter(unittest.TestCase):
    def setUp(self):
        self.maxValid = NUMBER_CANDIDATES
        self.candidates = [ make_candidate() for i in range( 0, NUMBER_CANDIDATES ) ]
        self.election = DO.OfficeElection(OFFICE_NAME, FIELD_NAME, self.candidates, self.maxValid)

    def test_initializes_properly(self):
        vc = P.VoteCounter(self.election)
        # Check that the counter for invalid results is set to 0
        self.assertEqual(vc.processingDict['invalid'], 0)
        # Check that all of the test names have been added
        # and that they have the count of 0
        for name in self.candidates:
            self.assertEqual(vc.processingDict[name], 0)

    def test_initialize_without_defined_candidates(self):
        # prep
        election = DO.OfficeElection(OFFICE_NAME, FIELD_NAME, [], self.maxValid)
        # call
        vc = P.VoteCounter(election)

        # check
        self.assertEqual(vc.processingDict['invalid'], 0, "invalid initialized properly")
        self.assertEqual(len(vc.processingDict.keys()), 1, 'no names in results dict')

    def test_one_candidate_gets_every_vote(self):
        """
        0 abstentions; 0 errors
        Each voter valid_votes for the same candidate
        """
        # prep
        luckyWinner = self.candidates[0]

        f = []
        for i in range(0, NUMBER_VOTERS):
            f.append({'rowId': i, FIELD_NAME: luckyWinner})
        testFrame = DataFrame(f)

        expected = {c: 0 for c in self.candidates}
        expected['invalid'] = 0
        expected[luckyWinner] = NUMBER_VOTERS

        # call
        vc = P.VoteCounter(self.election)
        vc.count(testFrame)

        # check
        for k in expected.keys():
            self.assertEqual(vc.processingDict[k], expected[k], " values are equal for %s" % k)

    def test_each_candidate_gets_one_vote(self):
        """
        0 abstentions; 0 errors
        Each voter valid_votes for one of the candidates; no two
        voters vote for the same candidate
        Thus each candidate's vote total is 1
        :return:
        """
        testFrame = []
        for i in range(0, NUMBER_CANDIDATES):
            testFrame.append({'rowId': i, FIELD_NAME: make_vote_string(self.candidates[i])})
        testFrame = DataFrame(testFrame)

        expected = {c: 1 for c in self.candidates}
        expected['invalid'] = 0

        # call
        vc = P.VoteCounter(self.election)
        vc.count(testFrame)

        # check
        for k in expected.keys():
            self.assertEqual(vc.processingDict[k], expected[k], " values are equal for %s" % k)

    def test_all_vote_for_all_candidates(self):
        """
        0 abstentions; 0 errors
        Each voter valid_votes for all of the candidates
        Thus each candidate's vote total is # voters
        """
        f = []
        for i in range(0, NUMBER_VOTERS):
            f.append({'rowId': i, FIELD_NAME: make_vote_string(self.candidates)})
        testFrame = DataFrame(f)

        expected = {c: NUMBER_VOTERS for c in self.candidates}
        expected['invalid'] = 0

        # call
        vc = P.VoteCounter(self.election)
        vc.count(testFrame)

        # check
        for k in expected.keys():
            self.assertEqual(vc.processingDict[k], expected[k], " values are equal for %s" % k)

    def test_candidate_wins_by_one_vote(self):
        """
        0 abstentions; 0 errors
        One voter only valid_votes for one candidate; every
        other voter vote for every candidate
        Thus the winner's total is 1 more than each of her competitors
        """
        # prep
        luckyWinner = self.candidates[0]
        f = []
        for i in range(0, NUMBER_VOTERS):
            record = {'rowId': i}
            if i == 0:
                # The first voter only valid_votes for the winner
                record[FIELD_NAME] = make_vote_string(luckyWinner)
            else:
                record[FIELD_NAME] = make_vote_string(self.candidates)
            f.append(record)
        testFrame = DataFrame(f)

        expected = {c: NUMBER_VOTERS - 1 for c in self.candidates}
        expected['invalid'] = 0
        expected[self.candidates[0]] = NUMBER_VOTERS

        # call
        vc = P.VoteCounter(self.election)
        vc.count(testFrame)

        # check
        for k in expected.keys():
            self.assertEqual(vc.processingDict[k], expected[k], " values are equal for %s" % k)

    def test_overselection_all_vote_for_too_many_candidates(self):
        """
        0 abstentions; 0 errors
        Each voter valid_votes for all of the candidates
        Thus each candidate's vote total is # voters
        """
        f = []
        for i in range(0, NUMBER_VOTERS):
            f.append({'rowId': i, FIELD_NAME: make_vote_string(self.candidates + self.candidates)})

        testFrame = DataFrame(f)
        expected = {c: 0 for c in self.candidates}
        expected['invalid'] = NUMBER_VOTERS

        # call
        vc = P.VoteCounter(self.election)
        vc.count(testFrame)

        # check
        for k in expected.keys():
            self.assertEqual(vc.processingDict[k], expected[k], " values are equal for %s" % k)

    def test_invalid_name_selection(self):
        pass


if __name__ == '__main__':
    unittest.main()

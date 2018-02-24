import unittest


import counter.DataObjects as DO
import counter.Processors as P


class VoteCounter(unittest.TestCase):
    def test_VoteCounter_initialization(self):
        testNames = ['smith, john (folks)', 'jip, receive (nosing)']
        maxValid = 2
        election = DO.OfficeElection('office1', 'field name', testNames, maxValid)

        vc = P.VoteCounter(election)
        # Check that the counter for invalid results is set to 0
        self.assertEqual(vc.resultsDict['invalid'],  0)
        # Check that all of the test names have been added
        # and that they have the count of 0
        for name in testNames:
            self.assertEqual(vc.resultsDict[name],  0)



if __name__ == '__main__':
    unittest.main()

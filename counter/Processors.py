"""
Created by adam on 2/5/18
"""
__author__ = 'adam'
from pandas import DataFrame
import counter.DataObjects as DO
import counter.Exceptions as EX
import counter.Helpers as HLP
import counter.FileSystemTools as FST


class VoteCounter(object):
    def __init__(self, electionObject):
        self.resultsFileName = "%s %s Results.xlsx" % (FST.getTimestampForMakingFileName(), electionObject.officeName)
        self.electionObject = electionObject
        self.candidates = electionObject.candidateNames
        self.maxValid = electionObject.maxValid
        self.resultsDict = {'invalid': 0}
        self._initialize_results_dict()

    def _initialize_results_dict(self):
        """Makes each candidate a key in the resultsDict with an initial total of 0"""
        for candidate in self.candidates:
            self.resultsDict[candidate] = 0

    def _process_selected_candidate(self, candidateName):
        """Takes a candidate name and adds 1 to the tally for that candidate"""
        # todo add test for validity
        self.resultsDict[candidateName] += 1

    def count(self, frame, outputFilePath):
        columnName = self.electionObject.fieldName
        for row in frame[columnName]:
            try:
                # Separate into a list of candidates the voter has chosen
                listOfSelectedNames = HLP.ResultFieldProcessor.process_field_values(row)
                # todo check if number of selected is wrong
                if self._is_list_valid(listOfSelectedNames):
                    # Update the tallys for the selected candidates
                    [self._process_selected_candidate(name) for name in listOfSelectedNames]
                else:
                    self._handle_overselection(listOfSelectedNames)
            except EX.VoterErrors:
                pass

        self._handle_count_complete(outputFilePath)

    def getResults(self):
        return self.resultsDict

    def _is_list_valid(self, resultList):
        """Applies the requisite tests to validate the list of results"""
        return len(resultList) <= self.maxValid

    def _handle_overselection(self, resultList):
        # increment the invalid list
        self.resultsDict['invalid'] += 1
        # logs
        raise EX.OverSelectionError(self.maxValid, resultList)

    def _handle_count_complete(self, outputFilePath):
        """Writes results to file"""
        resultsFile = '%s/%s' % (outputFilePath, self.resultsFileName)
        DataFrame(self.resultsDict, index=['totalVotes']).T.to_excel(resultsFile)


if __name__ == '__main__':
    pass

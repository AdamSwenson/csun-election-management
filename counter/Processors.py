"""
Created by adam on 2/5/18
"""
__author__ = 'adam'
from pandas import DataFrame
import counter.DataObjects as DO
import counter.Exceptions as EX
import counter.Helpers as HLP
import counter.FileSystemTools as FST
import counter.Loggers as LG


class VoteCounter(object):
    """This handles processing the election results"""

    def __init__(self, electionObject, **kwargs):
        """
        :param electionObject:
        """
        self.resultsFileName = "%s %s Results.xlsx" % (FST.getTimestampForMakingFileName(), electionObject.officeName)
        self.addNames = False
        self.electionObject = electionObject
        self.candidates = electionObject.candidateNames
        self.maxValid = electionObject.maxValid
        self.processing_event_logger = LG.ProcessingEventLogger()
        self.resultsDict = {'invalid': 0}
        self._process_kwargs(kwargs)
        self._initialize_results_dict()

    def _process_kwargs(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _initialize_results_dict(self):
        """Makes each candidate a key in the resultsDict with an initial total of 0"""
        for candidate in self.candidates:
            self._initialize_name(candidate)

    def _initialize_name(self, name):
        """Adds a candidate name to the results dict keys and sets its value to 0"""
        self.resultsDict[name] = 0

    def _process_selected_candidate(self, candidateName):
        """Takes a candidate name and adds 1 to the tally for that candidate"""
        self.resultsDict[candidateName] += 1

    def count(self, frame, outputFilePath=None):
        """
        Runs the actual counting of the votes
        :param frame:
        :param outputFilePath:
        :return:
        """
        columnName = self.electionObject.fieldName
        for idx, row in frame.iterrows():
            try:
                # Separate into a list of candidates the voter has chosen
                listOfSelectedNames = HLP.ResultFieldProcessor.process_field_values(row[columnName])
                # check if number of selected is wrong
                if self._is_list_valid(listOfSelectedNames):
                    # Update the tallys for the selected candidates
                    [self._process_selected_candidate(name) for name in listOfSelectedNames]
                else:
                    self._handle_overselection(listOfSelectedNames, row.rowId)
            except EX.VoterErrors:
                pass

        self._handle_count_complete(outputFilePath)

    def getResults(self):
        return self.resultsDict

    def _parse_selected_candidates(self, row):
        """ Separates the row into a list of candidates the voter has chosen
        If addNames has been checked, it will add the name to the results dict
        If not, it will raise an error
        """
        columnName = self.electionObject.fieldName
        listOfSelectedNames = HLP.ResultFieldProcessor.process_field_values(row[columnName])
        for name in listOfSelectedNames:
            self._validate_name(name)
        return listOfSelectedNames

    def _is_list_valid(self, resultList):
        """Applies the requisite tests to validate the list of results"""
        return len(resultList) <= self.maxValid

    def _validate_name(self, selectedName):
        """Checks that the name provided matches a key in the results
        dictionary. If the 'addNames' option has been selected, it adds the name
        to the keys instead of giving an error. Otherwise, it raises an error"""
        if selectedName in self.resultsDict.keys():
            return True

        if self.addNames:
            self._initialize_name(selectedName)
            return True

        raise EX.InvalidCandidateName(selectedName)

    def _handle_overselection(self, resultList, rowId):
        """This is called when a voter has selected too many names"""
        # increments the invalid list
        self.resultsDict['invalid'] += 1
        # logs the error
        raise EX.OverSelectionError(self.maxValid, resultList, self.electionObject.officeName, rowId)

    def _handle_count_complete(self, outputFilePath):
        """Any tasks to be handled once the counting is done
        should go here. These should include writing results to file
        """
        if outputFilePath:
            resultsFile = '%s/%s' % (outputFilePath, self.resultsFileName)
            DataFrame(self.resultsDict, index=['totalVotes']).T.to_excel(resultsFile)
            self.processing_event_logger('Results written to %s' % resultsFile)


if __name__ == '__main__':
    pass

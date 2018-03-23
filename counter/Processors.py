"""
Created by adam on 2/5/18
"""
__author__ = 'adam'
import pandas as pd
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
        """Whether to add names that weren't in the election object"""
        self.addNames = True

        self.electionObject = electionObject
        self.office = electionObject.officeName
        self.candidates = electionObject.candidateNames
        self.maxValid = electionObject.maxValid

        self.processing_event_logger = LG.ProcessingEventLogger()
        self.error_logger = LG.VoterErrorLogger()

        self.resultsDict = {'illegal-overselection': 0,
                            'abstentions': 0}

        self._process_kwargs(kwargs)
        self._initialize_results_dict()

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
                resultField = row[columnName]

                self._absention_guard(resultField)

                # Separate into a list of candidates the voter has chosen
                listOfSelectedNames = HLP.ResultFieldProcessor.process_field_values(resultField)

                # check if number selected is wrong
                self._overselection_guard(listOfSelectedNames)

                # If no errors were raised, we
                # update the tallys for the selected candidates
                [self._increment_candidate_tally(name) for name in listOfSelectedNames]

            except EX.OverselectionError as error:
                # Increment the overselection count
                self.resultsDict['illegal-overselection'] += 1
                # log
                self.error_logger.log(self.office, error.type, row.rowId,  error.message)

            except EX.AbstentionError as error:
                self.resultsDict['abstentions'] += 1
                # log
                self.error_logger.log(self.office, error.type, row.rowId, error.message)

            except EX.InvalidCandidateName:
                pass

        self._handle_count_complete(outputFilePath)

    def getResults(self):
        return self.resultsDict

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

    def _increment_candidate_tally(self, candidateName):
        """Takes a candidate name and adds 1 to the tally for that candidate"""
        # This will add the name if addNames is true or
        # raise an exception if not in list of names
        self._name_guard(candidateName)
        # increment the name
        self.resultsDict[candidateName] += 1

    # def _parse_selected_candidates(self, row):
    #     """ Separates the row into a list of candidates the voter has chosen
    #     If addNames has been checked, it will add the name to the results dict
    #     If not, it will raise an error
    #     """
    #     columnName = self.electionObject.fieldName
    #     listOfSelectedNames = HLP.ResultFieldProcessor.process_field_values(row[columnName])
    #     for name in listOfSelectedNames:
    #         self._name_guard(name)
    #     return listOfSelectedNames

    def _absention_guard(self, result):
        if pd.isna(result):
            # The error will handle logging to file
            raise EX.AbstentionError()

    def _name_guard(self, selectedName):
        """Checks that the name provided matches a key in the results
        dictionary. If the 'addNames' option has been selected, it adds the name
        to the keys instead of giving an error. Otherwise, it raises an error"""
        if selectedName in self.resultsDict.keys():
            return True

        if self.addNames:
            self._initialize_name(selectedName)
            return True

        raise EX.InvalidCandidateName(selectedName)

    def _overselection_guard(self, resultList):
        """Applies the requisite tests to validate the list of results"""
        if len(resultList) > self.maxValid:
            # The error will handle logging to file
            raise EX.OverselectionError(self.maxValid, len(resultList))

    def _compute_total_legal_votes(self):
        """All votes which indicate a preference are legal"""
        return sum(self.resultsDict.values()) - self.resultsDict['abstentions']

    def _handle_count_complete(self, outputFilePath):
        """Any tasks to be handled once the counting is done
        should go here. These should include writing results to file
        """
        self.resultsDict['totalVotesCast'] = sum(self.resultsDict.values())
        self.resultsDict['totalLegalVotes'] = self._compute_total_legal_votes()
        df = DataFrame(self.resultsDict, index=['votes']).T
        # add a percent of legal votes field
        df['% legal votes'] = df.apply(lambda x: x / x.totalLegalVotes)
        df.sort_values(by='votes', ascending=False, inplace=True)

        if self.electionObject.maxValid == 1:
            # remove a total of votes cast fields
            # these are only required for officer positions
            # since they must get more than 50% of the legal vote
            # todo Refactor so that don't have to do in this dumb order
            df.drop(['totalLegalVotes', 'totalVotesCast'], axis=0, inplace=True)
            df.drop(['% legal votes'], axis=1, inplace=True)

        if outputFilePath:
            resultsFile = '%s/%s' % (outputFilePath, self.resultsFileName)
            # write results to file
            df.to_excel(resultsFile)
            self.processing_event_logger.log('Results written to %s' % resultsFile)


if __name__ == '__main__':
    pass

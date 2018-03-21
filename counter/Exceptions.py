"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

from counter import Loggers


class Errors(Exception):
    def __init__(self):
        self.logger = Loggers.LogWriter()

    def logError(self):
        raise NotImplementedError


class VoterErrors(Errors):
    """
    Error objects which are raised when the Voter has done something
    which prevents her vote from being counted
    """

    def __init__(self):
        super().__init__()
        self.logger = Loggers.VoterErrorLogger()

    def logError(self):
        self.logger.log(self.officeName, self.errorTypeString, self.rowId, self.messageContent)
        # msg = "[%s] %s" % (self.errorTypeString, self.messageContent)
        # self.logger.write(msg)


class ProcessUserErrors(Errors):
    """
    Error objects which are raised when the person
    running the vote tallying process has made some mistake.
    """

    def __init__(self):
        super().__init__()

    def logError(self):
        msg = "[%s] %s" % (self.errorTypeString, self.messageContent)
        self.logger.write(msg)


class OverSelectionError(VoterErrors):
    """Raised when the voter has selected more than the
    allowed number of candidates"""

    def __init__(self, maxValid, resultList, officeName, rowId):
        """
        Writes error to log. Does nothing else.
        :param maxValid: Integer of the maximum candidates one could vote for
        :param resultList: List of candidates voted for
        """
        self.errorTypeString = "ERROR: Overselection"

        super().__init__()
        self.officeName = officeName
        self.rowId = rowId
        self.messageContent = "The voter was allowed to select %s names; they selected %s names: \n %s " % (
            maxValid, len(resultList), resultList)
        self.logError()

    def __repr__(self):
        return "%s" % self.message


class InvalidCandidateName(VoterErrors):
    """Raised when the voter has selected a name that was not on the list of allowed candidates"""

    def __init__(self, officeName, rowId, candidateName):
        """
        Writes error to log. Does nothing else.
        :type rowId: int
        :type candidateName: string

        """
        self.errorTypeString = "ERROR: Invalid name"

        super().__init__()
        self.officeName = officeName
        self.rowId = rowId
        self.messageContent = "The voter selected a valid name. Viz: %s " % candidateName
        self.logError()

    def __repr__(self):
        return "%s" % self.message


if __name__ == '__main__':
    pass

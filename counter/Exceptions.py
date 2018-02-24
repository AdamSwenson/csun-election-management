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
        self.logger = Loggers.LogWriter()

    def logError(self):
        msg = "[%s] %s" % (self.errorTypeString, self.messageContent)
        self.logger.write(msg)


class ProcessUserErrors(Errors):
    """
    Error objects which are raised when the person
    running the vote tallying process has made some mistake.
    """

    def __init__(self):
        super()

    def logError(self):
        msg = "[%s] %s" % (self.errorTypeString, self.messageContent)
        self.logger.write(self.msg)


class OverSelectionError(VoterErrors):
    """Raised when the voter has selected more than the
    allowed number of candidates"""

    def __init__(self, maxValid, resultList):
        """
        Writes error to log. Does nothing else.
        :param maxValid: Integer of the maximum candidates one could vote for
        :param resultList: List of candidates voted for
        """
        super().__init__()
        self.errorTypeString = "Invalid selection count"
        self.messageContent = "The voter was allowed to select %s names; they selected %s names \n %s " % (
            maxValid, len(resultList), resultList)
        self.logError()

    def __repr__(self):
        return "%s" % self.message


if __name__ == '__main__':
    pass

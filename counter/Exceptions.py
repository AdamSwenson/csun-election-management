"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

from counter import Loggers


class Errors(Exception):
    def __init__(self):
        self.logger = Loggers.LogWriter()

    # def logError(self):
    #     raise NotImplementedError


class VoterErrors(Errors):
    """
    Error objects which are raised when the Voter has done something
    which prevents her vote from being counted
    """
    #
    def __init__(self):
        super().__init__()


class OverselectionError(VoterErrors):
    """Raised when the voter selected more candidates than they were allowed"""

    def __init__(self, maxValid, numberSelected):
        super().__init__()
        self.type = "illegal-overselection"
        self.message = "The was allowed to select %s; they selected %s" % (maxValid, numberSelected)


class AbstentionError(VoterErrors):
    """Called when the voter cast no vote"""

    def __init__(self):
        super().__init__()
        self.type = 'Abstention'
        self.message = "The voter abstained"



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

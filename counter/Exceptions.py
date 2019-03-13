"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

from counter import Loggers


class Errors( Exception ):
    def __init__( self ):
        self.logger = Loggers.LogWriter()

    # def logError(self):
    #     raise NotImplementedError


class InvalidatesVote( Exception ):
    """If this class inherits from this, its
    presence should subtract 1 vote from the
    total number of valid votes
    """
    def __init__( self ):
        super().__init__()


class VoterErrors( Errors ):
    """
    Error objects which are raised when the Voter has done something
    which prevents her vote from being counted
    """
    def __init__( self ):
        super().__init__()


class OverselectionError( VoterErrors ):
    """Raised when the voter selected more candidates than they were allowed"""

    def __init__( self, maxValid, numberSelected ):
        super().__init__()
        self.type = "illegal-overselection"
        self.message = "The was allowed to select %s; they selected %s" % (maxValid, numberSelected)


class AbstentionError( VoterErrors, InvalidatesVote ):
    """Called when the voter cast no vote"""

    def __init__( self, rowId=None ):
        super().__init__()
        self.rowId = rowId
        self.type = 'Abstention'
        self.message = "The voter abstained"


class OfficeProcessingError( Errors ):
    def __init__( self, list_of_errors ):
        self.errors = list_of_errors


class ProcessUserErrors( Errors ):
    """
    Error objects which are raised when the person
    running the vote tallying process has made some mistake.
    """

    def __init__( self ):
        super().__init__()

    def logError( self ):
        msg = "[%s] %s" % (self.errorTypeString, self.messageContent)
        self.logger.write( msg )


class InvalidCandidateName( VoterErrors ):
    """Raised when the voter has selected a name that was not on the list of allowed candidates"""

    def __init__( self, officeName, rowId, candidateName ):
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

    def __repr__( self ):
        return "%s" % self.message


class VoteStuffingError( VoterErrors ):
    def __init__( self, rowId, candidates ):
        super().__init__()
        self.type = "vote-stuffing"
        self.rowId = rowId
        self.message = "[Possible vote-stuffing error] row {} selected {} ".format( rowId, candidates )

    def __str__( self ):
        return self.message


class WriteInDetected( Exception ):
    """Called when the voter has written one or more candidates in"""

    def __init__( self ):
        super().__init__()
        # self.candidates = candidates
        self.type = 'write-in'
        self.message = "The voter wrote candidates in"


if __name__ == '__main__':
    pass

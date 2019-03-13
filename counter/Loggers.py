"""
todo make sure spacing etc in log file is correct and includes the voter id


Created by adam on 2/5/18
"""
__author__ = 'adam'
import datetime
import os
from counter import environment as env

# from logbook import Logger
# from click_to_tabulate_votes import LOG_FOLDER_PATH


def getTimestampString():
    """Returns the standard string format of timestamp used in making a file name"""
    # return datetime.date.isoformat(datetime.now())
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def makeLogFilePath():
    """Returns the path to the logfile """
    timeString = datetime.datetime.now().strftime("%Y-%m-%d %H%M")
    LOG_FOLDER_PATH = "%s/Logs/" % os.getcwd()
    return "%s/%s processing-log.txt" % (LOG_FOLDER_PATH, timeString)


class LogWriter(object):
    """
    Parent class for loggers which write to a textfile
    """

    def __init__(self):
        self.logfile = makeLogFilePath()

    def write(self, stuff):
        with open(self.logfile, 'a') as f:
            # print(stuff)
            f.write(stuff)
            f.close()


class WriteInVoteLogger(LogWriter):
    def __init__(self):
        super().__init__()
        self.logfile = "%s/write-in-log.txt" % env.LOG_FOLDER_PATH

    def make_log_entry(self, officeName, rowId, list_of_candidates):
        """Creates text to be written in a standardized format"""
        candidate_string = ' '.join(list_of_candidates)
        return "\n [ {} ] [row # {}] {}  \n".format(officeName,  rowId, candidate_string)

    def log(self, officeName: str, rowId: int, list_of_candidates:list):
        """Actually writes the entry to the file
        :param rowId:
        :param message:
        :type eventType: str
        :param eventType:
        :type officeName: str
        """
        self.write(self.make_log_entry(officeName, rowId, list_of_candidates))


class VoterErrorLogger(LogWriter):
    def __init__(self):
        super().__init__()

    def make_log_entry(self, officeName, eventType, rowId, message):
        """Creates text to be written in a standardized format"""
        return "\n [ %s ] [ %s ] [row # %s] %s  %s \n" % (officeName,  eventType, rowId, getTimestampString(), message)

    def log(self, officeName: str, eventType: str, rowId: int, message:str):
        """Actually writes the entry to the file
        :param rowId:
        :param message:
        :type eventType: str
        :param eventType:
        :type officeName: str
        """
        self.write(self.make_log_entry(officeName, eventType, rowId, message))


class ProcessingEventLogger(LogWriter):
    """This handles logging ordinary (i.e., non-errors) events during processing """

    def __init__(self):
        super().__init__()

    def log(self, message):
        self.write(message)

    def log_processing_start(self, filePath, numberRows):
        self.log("\n ****************** %s ************" % getTimestampString())
        msg = "\n %s rows have been loaded from %s" % (numberRows, filePath)
        self.log(msg)

    def log_processing_stop(self, filePath, numberRows):
        msg = "\n %s rows have been processed from %s" % (numberRows, filePath)
        self.log(msg)

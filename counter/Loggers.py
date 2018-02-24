"""
Created by adam on 2/5/18
"""
__author__ = 'adam'
import os
# from logbook import Logger
# from click_to_tabulate_votes import LOG_FOLDER_PATH

import datetime


def getTimestampString():
    """Returns the standard string format of timestamp used in making a file name"""
    # return datetime.date.isoformat(datetime.now())
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")


def makeLogFilePath():
    LOG_FOLDER_PATH = "%s/Logs/" % os.getcwd()
    # return "%s/%s processing-log.txt" % ('/Logs',  getTimestampString())
    return "%s/%s processing-log.txt" % (LOG_FOLDER_PATH,  getTimestampString())


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


class ProcessingEventLogger(LogWriter):
    def __init__(self):
        super().__init__()

    def _log(self, message):
        self.write(message)

    def log_processing_start(self, filePath, numberRows):
        self._log("****************** %s ************ \n" % getTimestampString())
        msg = "%s rows have been loaded from %s" % (numberRows, filePath)
        self._log(msg)

    def log_processing_stop(self, filePath, numberRows):
        msg = "%s rows have been processed from %s" % (numberRows, filePath)
        self._log(msg)




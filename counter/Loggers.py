"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

# from logbook import Logger

from counter.environment import *


class LogWriter(object):
    """
    Parent class for loggers which write to a textfile
    """

    def __init__(self):
        self.logfile = LOG_FILE_PATH

    def write(self, stuff):
        with open(self.logfile, 'a') as f:
            f.write(stuff)
            f.close()


class LogHandler(object):
    def __init__(self):
        self.log_folder_path = ''

    def _log(self, message):
        print(message)

    def log_processing_start(self, filePath, numberRows):
        msg = "%s rows have been loaded from %s" % (numberRows, filePath)
        self._log(msg)

    def log_invalid_record(self, message):
        self._log(message)


if __name__ == '__main__':
    pass

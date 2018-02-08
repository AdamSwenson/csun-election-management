"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

import FileSystemTools

# Where the processor should look to find the files to proces
INPUT_FOLDER_PATH = "%s/Desktop/electionProcessing/input" % FileSystemTools.getSystemRoot()

# Where the files containing results and summary information are
# stored.
OUTPUT_FOLDER_PATH = "%s/Desktop/electionProcessing/output"  % FileSystemTools.getSystemRoot()

# Where to output the processing logs so that they may be audited
LOG_FOLDER_PATH = "%s/Desktop/electionProcessing/logs" % FileSystemTools.getSystemRoot()
LOG_FILE_PATH = "%s/Desktop/electionProcessing/logs/testlog.txt" % FileSystemTools.getSystemRoot()

if __name__ == '__main__':
    from Exceptions import *
    from DataObjects import *
    from Helpers import *
    from Processors import VoteCounter

"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

import datetime

# from FileSystemTools import getSystemRoot, getTimestampForMakingFileName


def getSystemRoot():
    """
    Returns the base directory path.
    On a Mac this is usually something like: 'Users/adam/'
    :rtype: string
    """
    return os.getenv("HOME")


def getTimestampForMakingFileName():
    """Returns the standard string format of timestamp used in making a file name"""
    # return datetime.date.isoformat(datetime.now())
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
#
#
# # Where the processor should look to find the files to proces
# INPUT_FOLDER_PATH = "%s/Desktop/electionProcessing/input" % getSystemRoot()
#
# # Where the files containing results and summary information are
# # stored.
# OUTPUT_FOLDER_PATH = "%s/Desktop/electionProcessing/output" % getSystemRoot()
#
# # Where to output the processing logs so that they may be audited
# LOG_FOLDER_PATH = "%s/Logs"
# # LOG_FOLDER_PATH = "%s/Desktop/electionProcessing/logs" % getSystemRoot()
# # LOG_FILE_PATH = "%s/Desktop/electionProcessing/logs/testlog.txt" % getSystemRoot()
#
# FILE_W_ROW_IDS_PATH = "%s/%s results_with_row_ids_added.csv" % (OUTPUT_FOLDER_PATH, getTimestampForMakingFileName())

if __name__ == '__main__':
    pass

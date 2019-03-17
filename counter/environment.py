"""
Created by adam on 2/5/18
"""
__author__ = 'adam'

import sys, os
import datetime


# The folder containing environment.py
PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
# Folders outside of the project foler
enclosing = os.path.abspath(os.path.dirname(PROJ_PATH))
sys.path.append(PROJ_PATH)
sys.path.append(enclosing)
from counter.FileSystemTools import getSystemRoot, getTimestampForMakingFileName
import Loggers as LG


try:
    assert(len(BASE) > 0)
except NameError:
    BASE = getSystemRoot()

# The folder containing environment.py
PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
# Folders outside of the project foler
enclosing = os.path.abspath(os.path.dirname(PROJ_PATH))
sys.path.append(PROJ_PATH)
sys.path.append(enclosing)


# Contains all data files and folders
DATA_FOLDER_PATH = "%s/Desktop/Election" % BASE

# Where the processor should look to find the files to proces
INPUT_FOLDER_PATH = "%s/input" % DATA_FOLDER_PATH
RESULTS_FOLDER_PATH = "%s/results" % INPUT_FOLDER_PATH
DEFINITIONS_FOLDER_PATH = "%s/definitions" % INPUT_FOLDER_PATH

# Where the files containing results and summary information are
# stored.
OUTPUT_FOLDER_PATH = "%s/output" % DATA_FOLDER_PATH

# Where to output the processing logs so that they may be audited
LOG_FOLDER_PATH = "%s/logs" % DATA_FOLDER_PATH

OUTPUT_FILE = "%s/Returns.xlsx" % OUTPUT_FOLDER_PATH


# Input files
# Where to find the files defining the elections to be tabulated
ELECTION_DEF_FILES_PATH = "%s/definitions" % INPUT_FOLDER_PATH

# Other specific files that will use
ELIGIBILITY_FILE_PATH = "%s/historical/Eligible voters.xlsx" % INPUT_FOLDER_PATH
PAST_RETURNS_FILE_PATH = "%s/historical/Election returns.xlsx" % INPUT_FOLDER_PATH

# Loggers
# This will handle recording ordinary (non-error) events during processing
eventLogger = LG.ProcessingEventLogger()
writeInLogger = LG.WriteInVoteLogger(LOG_FOLDER_PATH)



# electionReturnsFilePath = "%s/Election returns.xlsx" % electionFolder
# # Input files
# # Where to find the files defining the elections to be tabulated
# ELECTION_DEF_FILES_PATH = "%s/Election-definitions" % INPUT_FOLDER_PATH
#
# # Where to find the results downloaded from canvas
# DATA_FILES_PATH = "%s/Results-exported-from-canvas" % INPUT_FOLDER_PATH

# electionFolder = "%s/Desktop/ELECTION" % BASE

if __name__ == '__main__':
    pass

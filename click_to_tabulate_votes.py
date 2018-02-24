"""
Created by adam on 2/23/18
"""
__author__ = 'adam'
import os
from counter import FileSystemTools
from counter import Processors

# Where the processor should look to find the files to proces
INPUT_FOLDER_PATH = "%s/Input" % os.getcwd()

# Where the files containing results and summary information are
# stored.
OUTPUT_FOLDER_PATH = "%s/Output" % os.getcwd()

# Where to output the processing logs so that they may be audited
LOG_FOLDER_PATH = "%s/Logs" % os.getcwd()

# Input files
# Where to find the files defining the elections to be tabulated
ELECTION_DEF_FILES_PATH = "%s/Election-definitions" % INPUT_FOLDER_PATH

# Where to find the results downloaded from canvas
DATA_FILES_PATH = "%s/Results-exported-from-canvas" % INPUT_FOLDER_PATH

# Load the data from the csv file into a dataframe
data = FileSystemTools.load_results_into_frame(DATA_FILES_PATH)
# Give each row an id, starting with 0.
# This also saves a copy of the modified file to the log path for audits.
# That is useful because the log file will refer to these row ids
FileSystemTools.add_rowIds(data, LOG_FOLDER_PATH)

# Okay. We're now ready to get started.
# First, we load a list of election definitions
elections = []
# Walk the folder containing the election definition files and
# compile a list of filenames
fileList = FileSystemTools.makeDataFileList(ELECTION_DEF_FILES_PATH)
for f in fileList:
    elections.append(FileSystemTools.make_election_obj_from_file(f))

# The elections list is now populated with DataObject.OfficeElection objects
print('%s elections have been loaded' % len(elections))

# Now that we're ready to go, we perform the counts
# This is not part of the above loop to make logging
# and the addition of other validation steps easier
for election in elections:
    # Each time through we instatiate a new
    # vote counter object. That's important, fyi
    vc1 = Processors.VoteCounter(election)
    vc1.count(data, OUTPUT_FOLDER_PATH)

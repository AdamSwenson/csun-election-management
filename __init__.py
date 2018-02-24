import os

# Where the processor should look to find the files to proces
INPUT_FOLDER_PATH = "%s/Input" % os.getcwd()

# Where the files containing results and summary information are
# stored.
OUTPUT_FOLDER_PATH = "%s/Output" % os.getcwd()

# Where to output the processing logs so that they may be audited
LOG_FOLDER_PATH = "%s/Logs" % os.getcwd()

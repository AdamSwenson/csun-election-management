"""
Utillities for exploring the filesystem
Created by adam on 12/27/16
"""
__author__ = 'adam'

import os
import datetime

import counter.Loggers
# from Loggers import *

# from counter import Loggers
from counter import DataObjects, Loggers

import pandas as pd

# The file that will have the altered orginal with the row
# id numbers that are used in the logs.
FILE_W_ROW_IDS_NAME_BASE = "canvas_file_with_row_ids_added.xlsx"
RESULTS_NAME_BASE = "Vote Tallies.xlsx"


def add_rowIds(frame, outputFilePath=False):
    """Gives each row a unique id.
    Ids begin at 0
    If provided with a path to the output file, saves to that location
    """
    frame.reset_index(inplace=True)
    frame.rename({'index': 'rowId'}, axis=1, inplace=True)
    if outputFilePath:
        name = "%s %s" % (getTimestampForMakingFileName(), FILE_W_ROW_IDS_NAME_BASE)
        to = "%s/%s" % (outputFilePath, name)
        logger = Loggers.LogWriter()
        frame.to_excel(to)
        logger.write("Each row has been given an id. The modified sheet has been saved to %s" % name)


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


def load_results_into_frame(resultsFilePath):
    """Given a folder location, this reads the first file from csv into a
    pandas dataframe
    """
    logger = Loggers.ProcessingEventLogger()
    # fileList = makeDataFileList(resultsFilePath)
    return pd.read_csv(resultsFilePath)
    # frames = []
    # for f in fileList:
    #     dt = pd.read_csv(f)
        # logger.log_processing_start(fileList[0], len(dt))
        # frames.append(dt)
    # return pd.concat(frames)


def make_results_file_path(outputFilePath, officeName):
    return '%s/%s %s %s' % (outputFilePath, getTimestampForMakingFileName(), officeName, RESULTS_NAME_BASE)


def make_election_obj_from_file(fileName):
    """Reads an excel file definining an election and returns an OfficeElection object"""
    d = pd.read_excel(fileName)
    o = {
        'office': d['Office'][0],
        'canvas': d['Canvas column name'][0],
        'max': d['Maximum selections allowed'][0],
    }

    try:
        o['candidates'] = d['Candidate names'].tolist()
    except:
        o['candidates'] = []

    return DataObjects.OfficeElection(o['office'], o['canvas'], o['candidates'], o['max'])


def make_election_objects_from_file(fileName):
    """Reads an excel file definining several elections
     and returns a list of OfficeElection object"""
    d = pd.read_excel(fileName)
    objects = []
    for idx, row in d.iterrows():
        o = {
            'office': row['Office'],
            'canvas': row['Canvas column name'],
            'max': row['Maximum selections allowed'],
        }

        try:
            o['candidates'] = d['Candidate names'].tolist()
        except:
            o['candidates'] = []

        objects.append( DataObjects.OfficeElection(o['office'], o['canvas'], o['candidates'], o['max']))
    return objects


def makeDataFileList(folderPath, exclude=[]):
    """
    Returns a a list of all files in the source directory
    so that each file has its path appended to it.

    Args:
        folderPath: The path to get file names from
        exclude: file names which should not be included in the output list
    """
    exclude = exclude if any(exclude) else ['.DS_Store', '.gitignore']
    datafiles = []
    for root, dirs, files in os.walk(folderPath):
        for name in files:
            if name not in exclude:
                datafiles.append(os.path.join(root, name))

    return datafiles


def makeDataFileIterator(folderPath, exclude=[]):
    """
    Returns an iterator of all files in the source directory
    so that each file has its path appended to it.

    Args:
        folderPath: The path to get file names from
        exclude: file names which should not be included in the output list
    """
    exclude = exclude if any(exclude) else ['.DS_Store']
    for root, dirs, files in os.walk(folderPath):
        for name in files:
            if name not in exclude:
                yield os.path.join(root, name)


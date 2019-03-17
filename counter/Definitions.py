"""
Created by adam on 3/12/19
"""
__author__ = 'adam'
import pandas as pd

import counter.environment as env
from counter.FileSystemTools import makeDataFileList


class OfficeDefinitions( object ):

    def __init__( self,  definition_filepath, election ):
        self.election = election
        self.def_map = {
            'office': [ 'Office', 'office' ],
            'field': [ 'Canvas column name', 'Results column name' ],
            'max': [ 'Maximum selections allowed' ],
            'requires_maj': [ 'Requires majority' ]
        }

        self._load( definition_filepath )

    def _load( self, definitions_filepath ):
        # print(definitions_filepath)
        # files = [ f for f in makeDataFileList( definitions_folder ) if f[ -4: ] == 'xlsx' or f[ -3: ] == 'xls' ]
        #
        # if election == 'general':
        #
        # # frames = []
        # # for f in files:
        # #     frames.append(pd.read_excel( f ))
        # # self.defs = pd.merge(frames)

        # Standardize column names
        self.defs = pd.read_excel( definitions_filepath )
        for k in self.def_map.keys():
            for c in self.def_map[ k ]:
                if c in self.defs.columns:
                    self.defs.rename( { c: k }, axis=1, inplace=True )

    def get_office_name_for_field( self, field ):
        return self.defs.set_index( 'field' ).loc[ field ][ 'office' ]

    def office_requires_majority( self, field ):
        v = self.defs.set_index( 'field' ).loc[ field ][ 'requires_maj' ]
        return v in ['Yes', 'yes', 'Y', 'T', 'True', 1 ]



if __name__ == '__main__':
    pass

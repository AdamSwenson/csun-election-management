# Tools for administering CSUN's faculty elections

## Setup instructions
Create a folder named ....

# Inputs

## Election definition files
Location: Input/Election-definitions
Purpose: Each election needs to have an election definition file. The program will read the values from this file and process the appropriate column in the voting results accordingly

Format: These should follow the format in Input/election-definition-template.xlsx

These should be excel files (preferably xlsx)

Each file should define the following :

        Office
        	   This is the name of the office the election is for.
        
        Canvas column name	
                The string of text which appears in the header row of the output from Canvas. It will look something like this: 
        
                    953897: Choose 2 (ONLY 2) of the following:
        
                Make sure you use the entire thing, including the trailing punctuation.

        
        Maximum selections allowed
        	This should be an integer value
        	If a voter selects more than this number, their vote will be disqualified.
        	
        
        Candidate names
            All valid names (as they  will appear in the results downloaded from canvas) should appear in this column. No more than one name should appear on any row.
            Do not leave blank rows.
       

## Results exported from canvas
These are the results which we are going to process. There should be only one file in this folder.


# Outputs
The program will produce a file in the Output folder
Name : 


# Log files
Two kinds of log files will be produced. 
One is an excel file which is just a copy of the initial input file, but
with row id numbers inserted. This will be helpful for auditing because
the row id numbers will be used to identify rows in the other log file.

The second is a text file. This is the log of everything which happened during
processing the votes.
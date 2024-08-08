'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-30 12:17:51
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-30 12:18:17
 # @ Description: 
        This file should contain functions that handle the 
        flow of the program. Additional responisibilities 
        should be handed off to other files, such as insertion
        and sanitization.
 '''

### External Imports ###

import logging
import os

### Internal Imports ###

from config.states import FileStateHolder, FileStates
from utility.file.fileload import loadDataframeCSV, loadDataframeXLSX
from handler.stateHandler import changeFileState

### Function Declarations ###
    

def handleFile(filepaths):
    for i in range(len(filepaths)):
        fileState = FileStateHolder()
        currentFilepath = filepaths[i]
        df = None
        logging.info(f'Handling file {i+1} of {len(filepaths)}: {currentFilepath}')
        while fileState.getState() != FileStates.END:

            match fileState.getState():

                case FileStates.INITIALIZATION:
                    match os.path.splitext(currentFilepath)[1]:
                        case 'xlsx':
                            df = loadDataframeXLSX(currentFilepath)
                        case 'csv':
                            df = loadDataframeCSV(currentFilepath, ',')
                        case 'txt':
                            pass
                        case _:
                            logging.error(f'Unsupported file extension: {os.path.splitext(currentFilepath)[1]}')
                            fileState.setState(FileStates.END)
            
                case FileStates.LOADING:
                    pass

                case FileStates.STAGING:
                    pass

                case FileStates.MERGE:
                    pass
            
            changeFileState(fileState)
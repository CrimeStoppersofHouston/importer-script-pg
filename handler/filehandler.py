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
import threading

### Internal Imports ###

from config.flagParser import FlagParser
from config.states import FileStateHolder, FileStates
from handler.stateHandler import changeFileState
from model.database import hcdcSnapshot
from model.fileModel import HCDCModel
from utility.connection.connectionPool import ConnectionPool
from utility.file.fileload import loadDataframeCSV, loadDataframeXLSX
from automation.schema_creation import hcdc_snapshot

### Function Declarations ###
    

def handleFile(filepaths):
    parser = FlagParser()
    connectionPool = ConnectionPool(
        os.getenv('USERNAME'),
        os.getenv('PASSWORD'),
        os.getenv('SERVER'),
        os.getenv('PORT'),
        os.getenv('DATABASE'),
        os.getenv('DRIVER')
    )
    match parser.args.type:
        case 'hcdc':
            connectionPool.addConnection()
            conn = connectionPool.getAvailableConnection()
            hcdc_snapshot.create(os.getenv('DATABASE'), conn, connectionPool)
            connectionPool.clear()

    for i in range(len(filepaths)):
        fileState = FileStateHolder()
        fileState.setState(FileStates.INITIALIZATION)
        currentFilepath = filepaths[i]
        model = None
        df = None
        logging.info(f'Handling file {i+1} of {len(filepaths)}: {currentFilepath}')
        while fileState.getState() != FileStates.END:

            match fileState.getState():

                case FileStates.INITIALIZATION:
                    pass
            
                case FileStates.LOADING:
                    logging.info('Loading file...')
                    match os.path.splitext(currentFilepath)[1]:
                        case 'xlsx':
                            df = loadDataframeXLSX(currentFilepath)
                        case 'csv':
                            df = loadDataframeCSV(currentFilepath, parser.args.delimiter)
                        case 'txt':
                            df = loadDataframeCSV(currentFilepath, parser.args.delimiter)
                        case _:
                            logging.error(f'Unsupported file extension: {os.path.splitext(currentFilepath)[1]}')
                            fileState.setState(FileStates.END)
                    logging.info(f'{currentFilepath} loaded successfully!')

                case FileStates.SANITIZATION:
                    logging.info('Sanitizing columns for insertion...')
                    match parser.args.type:
                        case 'hcdc':
                            for column in HCDCModel.conversions:
                                df[column] = df[column].apply(lambda x: HCDCModel.conversions[column](x))
                            model = hcdcSnapshot.database
                        case _:
                            raise ValueError(f'Unimplemented format: {parser.args.type}')
                    logging.info('All columns sanitized!')

                case FileStates.STAGING:
                    while not model.isCompleted():
                        table = model.getAvailableTable()
                        if table is None:
                            continue

                        if len(connectionPool.availableConnections) == 0 and len(connectionPool.pool) < connectionPool.max_connections:
                            connectionPool.addConnection()

                        if connectionPool.availableConnections > 0:
                            connection = connectionPool.getAvailableConnection()
                            # threading.run(insert(df, table, conneciton, connectionPool))

                    connectionPool.clear()

                case FileStates.MERGE:
                    while not model.isCompleted():
                        table = model.getAvailableTable()
                        if table is None:
                            continue

                        if len(connectionPool.availableConnections) == 0 and len(connectionPool.pool) < connectionPool.max_connections:
                            connectionPool.addConnection()

                        if connectionPool.availableConnections > 0:
                            connection = connectionPool.getAvailableConnection()
                            # threading.run(merge(df, table, conneciton, connectionPool))
                    
                    connectionPool.clear()
            
            changeFileState(fileState)
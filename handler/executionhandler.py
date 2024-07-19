'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-30 14:17:55
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-06-20 10:22:01
 # @ Description: 
    Links execution functions to their respective execution stages. This design
    should allow for easy customization of program behavior.
 '''

### External Imports ###

import logging
import time
from datetime import datetime
import sys
import os

### Internal Imports ###

from automation.hcdcDatasetsGathering import runPlaywright
from config.flagParser import FlagParser
from config.states import ProgramStateHolder, ProgramStates
from handler.stateHandler import changeProgramState
from utility.file.filefetch import fetchFromDirectory
from utility.file.filefetch import hcdcFileValidation

### Function Declarations ###


def executeProgram():
    filepaths = []
    parser = FlagParser()
    programState = ProgramStateHolder()
    while programState.currentState != ProgramStates.END:
        match programState.currentState:

            case ProgramStates.INITIALIZATION:
                for handler in logging.root.handlers[:]:
                    logging.root.removeHandler(handler)
                logging.basicConfig(level=logging.INFO if not parser.args.debug else logging.DEBUG, 
                                    format='%(asctime)s\t[%(levelname)s]\t%(message)s',
                                    handlers=[
                                        logging.FileHandler(f"./logs/{datetime.now().strftime('debug_%Y%m%d_%H%M')}.log"),
                                        logging.StreamHandler(sys.stdout)
                                    ])
                logging.debug('Entering debug mode...')
                logging.info('Initialization complete!')

            case ProgramStates.FILE_FETCH:
                logging.info('Fetching filepaths...')
                if parser.args.directory:
                    try:
                        filepaths = fetchFromDirectory(parser.args.directory, parser.args.extension, parser.args.recursive, parser.args.depth)
                    except ValueError as e:
                        logging.error(f'Invalid argument supplied: {e}')
                    except Exception as e:
                        logging.error(f'Unexpected error while fetching filepaths: {e}')

                elif parser.args.file:
                    if os.path.exists(parser.args.file):
                        filepaths.append(parser.args.file)
                    else:
                        logging.error(f'Invalid filepath supplied: {parser.args.file}')
                
                elif parser.args.hcdc:
                    try:
                        if parser.args.collect:
                            runPlaywright()
                        filepaths, code = hcdcFileValidation(parser.args.hcdc, parser.args.debug)
                    except ValueError as e:
                        logging.error(f'Invalid argument supplied: {e}')
                    except Exception as e:
                        logging.error(f'Unexpected error while fetching HCDC records: {e}')
                        
                if len(filepaths) == 0:
                    logging.error(f'No files were found!')
                    exit(1)

                logging.debug(f'{len(filepaths)} files were found: {filepaths}')
                logging.info(f'{len(filepaths)} files fetched')

            case ProgramStates.FILE_PROCESSING:
                pass

            case ProgramStates.REPORTING:
                pass
        
        changeProgramState(programState)
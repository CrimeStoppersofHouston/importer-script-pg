'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-06-21 12:16:55
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-06-21 12:16:57
 # @ Description: 
    This file should contain the handler functions needed
    to change the state of the program. The process for changing
    the way the program operates should remain easy to understand
    and tweak as needed. This design should allow for easy integration
    of new functionalities as needed.
 '''

### Internal Imports ###

from config.states import FileStates, ProgramStates, FileStateHolder, ProgramStateHolder

### Function Declarations ###


def changeProgramState(pstate: ProgramStateHolder):
    match pstate.getState():
        case ProgramStates.INITIALIZATION:
            pstate.setState(ProgramStates.FILE_FETCH)

        case ProgramStates.FILE_FETCH:
            pstate.setState(ProgramStates.FILE_PROCESSING)

        case ProgramStates.FILE_PROCESSING:
            pstate.setState(ProgramStates.REPORTING)

        case ProgramStates.REPORTING:
            pstate.setState(ProgramStates.END)


def changeFileState(fstate: FileStateHolder):
    match fstate.getState():
        case FileStates.INITIALIZATION:
            fstate.setState(FileStates.SANITIZATION)

        case FileStates.LOADING:
            fstate.setState(FileStates.SANITIZATION)

        case FileStates.SANITIZATION:
            fstate.setState(FileStates.STAGING)

        case FileStates.STAGING:
            fstate.setState(FileStates.MERGE)

        case FileStates.MERGE:
            fstate.setState(FileStates.END)
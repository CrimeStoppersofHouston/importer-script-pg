'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-23 16:08:55
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-30 13:51:49
 # @ Description:
        This file contains the classes and enums for the
        states that the program can enter. This file should
        only contain resposibilities that are related to
        switching and reading the states of these classes
 '''

### External Imports ###

from enum import Enum
import logging

### Class Declarations ###

class State(Enum):
    pass

class ProgramStates(State):
    INITIALIZATION = 100
    FILE_FETCH = 101
    FILE_PROCESSING = 102
    REPORTING = 103
    END = 110

class FileStates(State):
    INITIALIZATION = 200
    LOADING = 201
    SANITIZATION = 202
    STAGING = 203
    MERGE = 204
    END = 210

class StateHolder():
    currentState = None

    def __init__(self, stateType:State):
        self.stateType = stateType 
    
    def setState(self, state:State):
        if state not in self.stateType:
            raise ValueError(f'Invalid State: {state}')
        logging.debug(f'Entering state: {state}')
        self.currentState = state

    def getState(self):
        return self.currentState

class FileStateHolder(StateHolder):
    # Singleton instance to avoid creating multiple instances
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(FileStateHolder, self).__new__(self)
        return self.instance
    
    def __init__(self):
        super().__init__(FileStates)
        self.setState(FileStates.INITIALIZATION)

class ProgramStateHolder(StateHolder):
    # Singleton instance to avoid creating multiple instances
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(ProgramStateHolder, self).__new__(self)
        return self.instance
    
    def __init__(self):
        super().__init__(ProgramStates)
        self.setState(ProgramStates.INITIALIZATION)
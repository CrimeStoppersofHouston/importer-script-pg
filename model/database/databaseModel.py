'''
# @ Author: Ryan Barnes
# @ Create Time: 2024-07-18 12:05:46
# @ Modified by: Ryan Barnes
# @ Modified time: 2024-07-18 12:08:24
# @ Description: 
    This file should contain the base classes for creating a model for
    a mysql database. It should be able to be used for insertion, creation,
    and merging queries. It should also be able to be used to define
    The relationships between tables so that insertion order may be determined
    automatically.
'''

### External Imports ###

from typing import Self, Type
from enum import Enum
import numpy as np
import logging
import builtins

### Internal Imports ###

from utility import conversionFunctions

### Class Declarations ###

class Column:
    '''Represents a column for mapping file columns to database columns'''
    def __init__(self, rawName: str, name: str, dataType: Type, **kwargs):
        self.rawName = rawName
        self.name = name
        self.dataType = dataType
        if kwargs.get('conversionFunction'):
            self.conversionFunction = kwargs.get('conversionFunction')
        else:
            match dataType:
                case builtins.str:
                    self.conversionFunction = conversionFunctions.convertToString
                case builtins.int:
                    self.conversionFunction = conversionFunctions.convertToInteger
                case np.datetime64:
                    self.conversionFunction = conversionFunctions.convertToDatetime
                case builtins.float:
                    self.conversionFunction = conversionFunctions.convertToFloat
                case _:
                    self.conversionFunction = None
                    logging.error(f'There is not an automatic implementation for {dataType.__name__} type')
                    raise ValueError()

class TableStatus(Enum):
    '''Helper class for marking table handling status'''
    PENDING = 1
    INPROGRESS = 2
    COMPLETED = 3

class Table:
    '''Represents a table containing rows'''
    def __init__(self, name: str):
        self.name = name
        self.columns = set()
        self.prereqs = set()
        self.status = TableStatus.PENDING


    def addColumn(self, column: Column) -> Self:
        '''Adds a column to the columns dict'''
        self.columns.add(column)
        return self


    def addPrereq(self, table: Self) -> Self:
        '''Adds a prerequisite table to be handled before this one'''
        self.prereqs.add(table)
        return self


    def advanceState(self):
        match self.status:
            case TableStatus.PENDING:
                self.status = TableStatus.INPROGRESS
            case TableStatus.INPROGRESS:
                self.status = TableStatus.COMPLETED
            case TableStatus.COMPLETED:
                logging.warning("Advancing table status when already completed!")
                
                
    def getConversionDict(self) -> dict:
        returnDict = {}
        for column in self.columns:
            returnDict[column.rawName] = column.conversionFunction
        return returnDict
            

class Schema:
    
    def __init__(self, name: str):
        self.name = name
        self.completedTables = set()
        self.processingTables = set()
        self.pendingTables = set()
        self.tables = set()


    def getConversionDict(self):
        returnDict = {}
        for table in self.tables:
            conversionDict = table.getConversionDict()
            for duplicate in set(conversionDict.keys()).intersection(returnDict.keys()):
                if returnDict[duplicate] != conversionDict[duplicate]:
                    logging.error(f'Table {table.name} caused conversion function conflict on column {duplicate}')
                    raise Exception(f'Conversion function conflict on column {duplicate}')
            returnDict.update(table.getConversionDict())
        return returnDict


    def resetSchema(self):
        self.completedTables = set()
        self.processingTables = set()
        self.pendingTables = self.tables.copy()


    def getTablebyName(self, name: str) -> Table:
        '''returns a Table object if it exists in the Schema object'''
        return next((table for table in self.tables if table.name == name), None)


    def addTable(self, table: Table) -> Self:
        self.tables.add(table)
        self.pendingTables.add(table)
        return self


    def isCompleted(self):
        return self.completedTables.issubset(self.tables)
    

    def advanceTableState(self, table: Table):
        table.advanceState()
        match table.status:
            case TableStatus.INPROGRESS:
                self.pendingTables.remove(table)
                self.processingTables.add(table)
            case TableStatus.COMPLETED:
                self.processingTables.remove(table)
                self.completedTables.add(table)
            case _:
                logging.warning(f'Unaccounted table status {table.status} in {table.name}')


    def getAvailableTable(self) -> Table:
        if not self.pendingTables:
            logging.debug("There are no pending tables")
            return None
        for table in self.pendingTables:
            if table.prereqs.issubset(self.completedTables):
                self.advanceTableState(table)
                return table
            logging.debug(f'Cannot handle {table.name}, not all prerequisites are completed')
        logging.debug("There are no tables that can be handled")
        return None
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
import logging

### Internal Imports ###

from utility.conversionFunctions import convertSPN, convertToDatetime, convertToString, convertToInteger

### Class Declarations ###

class Column:
    '''Represents a column for mapping file columns to database columns'''
    def __init__(self, rawName: str, name: str, dataType: Type):
        self.rawName = rawName
        self.name = name
        self.dataType = dataType

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


    def addColumn(self, column: Column) -> None:
        '''Adds a column to the columns dict'''
        self.columns.add(column)


    def addPrereq(self, table: Self) -> None:
        '''Adds a prerequisite table to be handled before this one'''
        self.prereqs.add(table)


    def advanceState(self):
        match self.status:
            case TableStatus.PENDING:
                self.status = TableStatus.INPROGRESS
            case TableStatus.INPROGRESS:
                self.status = TableStatus.COMPLETED
            case TableStatus.COMPLETED:
                logging.warning("Advancing table status when already completed!")

class Schema:
    
    def __init__(self, name: str):
        self.name = name
        self.completedTables = set()
        self.processingTables = set()
        self.pendingTables = set()
        self.tables = set()


    def addTable(self, table: Table) -> None:
        self.tables.add(table)
        self.pendingTables.add(table)


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
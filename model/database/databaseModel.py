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

from typing import Self, Callable
from enum import Enum

### Internal Imports ###

from utility.conversionFunctions import convertSPN, convertToDatetime, convertToString, convertToInteger

### Class Declarations ###

class Column:
    '''Represents a column for mapping file columns to database columns'''
    def __init__(self, rawName: str, name: str):
        self.rawName = rawName
        self.name = name

class TableStatus(Enum):
    '''Helper class for marking table handling status'''
    PENDING = 1
    INPROGRESS = 2
    COMPLETED = 3

class Table:
    '''Represents a table containing rows'''
    def __init__(self, name: str):
        self.name = name
        self.columns = {}
        self.prereqs = set()
        self.status = TableStatus.PENDING


    def addColumn(self, column: Column) -> None:
        '''Adds a column to the columns dict'''
        self.columns[column.name] = column


    def addPrereq(self, table: Self) -> None:
        '''Adds a prerequisite table to be handled before this one'''
        self.prereqs.add(table)

class Schema:
    
    def __init__(self, name: str):
        self.name = name
        self.completedTables = set()
        self.pendingTables = []
        self.tables = set()


    def addTable(self, table: Table) -> None:
        self.uncompletedTables.append(table)


    def getAvailableTable(self) -> Table:
        if self.pendingTables:
            pass
        for table in self.uncompletedTables:
            pass
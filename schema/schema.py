'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-20 15:02:43
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-29 15:42:26
 # @ Description: 
        This file contains the base model class declarations
        used to create a full schema. This should allow for
        the compilation of table and column names, as well as
        their data types and conversion functions.
 '''

### External Imports ###

from datetime import datetime
import logging

### Internal Imports ###

from utility.conversionFunctions import convertToString, convertToInteger, convertToDatetime
from typing import Self, Callable

### Class Declarations ###

class Column():
    def __init__(self, name: str, datatype: type, originalName: str, conversionFunction: Callable = None):
        self.name = name
        self.datatype = datatype
        self.originalName = originalName

        if conversionFunction is None:
            match datatype:
                case str():
                    conversionFunction = convertToString
                case int():
                    conversionFunction = convertToInteger
                case datetime():
                    conversionFunction = convertToDatetime
                case _:
                    conversionFunction = convertToString

        self.conversionFunction = conversionFunction

        self.presentInImport = self.originalName != ''

class Table():
    def __init__(self, name: str, stage: str, isImportTable: bool = True):
        self.name = name
        self.stage = stage
        self.isImportTable = isImportTable

        self.columns = {}
    
    def addColumn(self, column:Column):
        self.columns[column.name] = column
        if self.isImportTable and not column.presentInImport:
            raise Exception(f'Import table {self.name} cannot have a column {column.name} which is not present within the data!')
        return self

class Schema():
    def __init__(self, name: str, server: str, port: int):
        self.name = name
        self.server = server
        self.port = port

        # Implementing this in a list format to allow for customization
        # in insertion order.
        self.tables = []

    def addTable(self, table: Table) -> Self:
        self.tables.append(table)
        return self
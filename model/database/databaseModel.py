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

### Internal Imports ###

from utility.conversionFunctions import convertSPN, convertToDatetime, convertToString, convertToInteger

### Class Declarations ###

class Schema:
    pass

class Table:
    pass

class Column:
   def __init__(self, rawName, name, conversionFunction: Callable = convertToString):
        self.rawName = rawName
        self.name = name
        self.conversionFunction = conversionFunction

        return self
    
   
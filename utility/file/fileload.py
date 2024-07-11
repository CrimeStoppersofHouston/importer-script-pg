'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-06-21 11:05:45
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-06-21 11:05:50
 # @ Description: 
    This file contains the functions needed to load various file extensions
    into pandas dataframes. Further cleaning and validations should be 
    handed off to other files. Ideally, these loads should not do any conversions
    whatsoever, to avoid unforseen problems with data formatting.
 '''

### External Imports ###

import os
import contextlib
import pandas as pd

### Function Declarations ###

def loadDataframeCSV(filepath) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise ValueError(f'File {filepath} does not exist')
    
    with contextlib.closing(open(filepath, 'r')) as f:
        return pd.read_csv(f, dtype=str)

def loadDataframeTSV(filepath) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise ValueError(f'File {filepath} does not exist')
    
    with contextlib.closing(open(filepath, 'r')) as f:
        return pd.read_csv(f, sep='\t', dtype=str)  

def loadDataframeGeneric(filepath, separator):
    if not os.path.exists(filepath):
        raise ValueError(f'File {filepath} does not exist')
    
    with contextlib.closing(open(filepath, 'r')) as f:
        return pd.read_csv(f, sep=separator, dtype=str)  

def loadDataframeXLSX(filepath) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise ValueError(f'File {filepath} does not exist')
    
    with contextlib.closing(open(filepath, 'r')) as f:
        return pd.read_excel(filepath, dtype=str)
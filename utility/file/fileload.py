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
import numpy as np

### Function Declarations ###

def loadDataframeCSV(filepath, delimiter:str = ',') -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise ValueError(f'File {filepath} does not exist')
    try:
        with contextlib.closing(open(filepath, 'r')) as f:
            df = pd.read_csv(f, sep=delimiter, dtype=str)
            df = df.replace(np.nan, None)
            return df
    except Exception as e:
        raise Exception(f'Cannot read CSV file: {e}')

def loadDataframeXLSX(filepath) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise ValueError(f'File {filepath} does not exist')
    try:
        with contextlib.closing(open(filepath, 'r')) as f:
            df = pd.read_excel(f, dtype=str)
            df = df.replace(np.nan, None)
            return df
    except Exception as e:
        raise Exception(f'Cannot read excel file: {e}')
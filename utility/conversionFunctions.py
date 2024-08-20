'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-23 14:38:08
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-29 11:06:16
 # @ Description:
        This file contains all of the functions used in
        converting dataframe columns to their correct
        data types.
 '''

### External Imports ###

from datetime import datetime
from sqlescapy import sqlescape

### Function Declarations ###

def convertToString(self, value, noneValue = None) -> str:
    if value is None or str(value).strip() == '':
        return noneValue
    return sqlescape(str(value).strip())


def convertToInteger(self, value, noneValue = None) -> int:
    if value is None or str(value).strip() == '':
        return noneValue
    return int(float(value))


def convertToDatetime(self, value, noneValue = None, dateFormat:str = "%Y%m%d") -> datetime:
    if value is None or str(value).strip() == '':
        return noneValue
    # Trim whitespace in order to avoid conversion errors
    value = str(value).strip()
    return datetime.strptime(value, dateFormat)


def convertToFloat(self, value, noneValue = None):
    if value is None or str(value).strip() == '':
        return noneValue
    return float(value)
    

def convertSPN(self, value, noneValue = None):
    if value is None or str(value).strip() == '':
        return noneValue
    return str(value).strip().zfill(8)

# This file contains all of the functions used in
# converting dataframe columns to their correct
# data types.

### External Imports ###

import pandas as pd
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

def convertSPN(self, value, noneValue = None):
    if value is None or str(value).strip() == '':
        return noneValue
    return str(value).strip().zfill(8)

### Variable Declarations ###

default_conversions = {
    str: convertToString,
    int: convertToInteger
}
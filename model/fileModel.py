'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-07-11 10:03:44
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-07-19 11:17:04
 # @ Description: 
    This file should contain the classes needed to standardize
    the conversion of loaded dataframes to standardized models
 '''

### External Imports ###

import pandas as pd

### Internal Imports ###

from utility.conversionFunctions import convertToDatetime, convertToString, convertToInteger, convertSPN

### Class Declarations ###

class FileModel:
    def __init__(self, neededColumns, conversions):
        self.neededColumns = neededColumns
        self.conversions = conversions


class HCDCModel(FileModel):
    def __init__(self):
        super().__init__(
            [
                # Lookup values
                'curr_off',
                'curr_off_lit',
                'aty_coc',
                'aty_coc_lit',
                'aty_spn',
                'aty_nam',
                
                # Defendant values
                'def_spn',
                'def_nam',
                'def_rac',
                'def_sex',
                'def_dob',
                'def_stnum',
                'def_stnam',
                'def_cty',
                'def_st',
                'def_zip',
                'def_citizen',

                # Report values
                'off_rpt_num',
                'comp_agency',
                'comp_nam',

                # Case values
                'cas',
                'fda',

                # Event values
                'dispdt',
                'cdi',
                'cad',
                'disposition',
                'sentence',
                'bam',
                'bamexp',
                'nda',
                'cst',
                'dst',
                'crt',
                'ins',
                'rea',
                'curr_l_d',
                'cnc'
            ],
            {
                # Lookup values
                'curr_off': lambda x: -1 if x is None or str(x).strip() == '' or pd.isna(x) else x,
                'curr_off_lit': convertToString,
                'aty_coc': convertToString,
                'aty_coc_lit': convertToString,
                'aty_spn': lambda x: str(x).zfill(8) if x is not None and str(x).strip() != '' and not pd.isna(x) else None,
                'aty_nam': convertToString,
                
                # Defendant values
                'def_spn': lambda x: str(x).zfill(8) if x is not None and str(x).strip() != '' and not pd.isna(x) else None,
                'def_nam': convertToString,
                'def_rac': convertToString,
                'def_sex': convertToString,
                'def_dob': convertToDatetime,
                'def_stnum': convertToString,
                'def_stnam': convertToString,
                'def_cty': convertToString,
                'def_st': convertToString,
                'def_zip': convertToString,
                'def_citizen': convertToString,

                # Report values
                'off_rpt_num': convertToString,
                'comp_agency': convertToString,
                'comp_nam': lambda x: convertToString(x) if x is not None and str(x).strip() != '' and not pd.isna(x) else None,

                # Case values
                'cas': convertToInteger,
                'fda': convertToDatetime,

                # Event values
                'dispdt': convertToDatetime,
                'cdi': convertToInteger,
                'cad': convertToString,
                'disposition': lambda x: convertToString(x) if x is not None and str(x).strip() != '' and not pd.isna(x) else None,
                'sentence': convertToString,
                'bam': lambda x: convertToInteger(float(x)) if x is not None and str(x).strip().isnumeric() and str(x).strip() != '' else x,
                'bamexp': convertToString,
                'nda': convertToDatetime,
                'cst': convertToString,
                'dst': convertToString,
                'crt': convertToInteger,
                'ins': convertToString,
                'rea': convertToString,
                'curr_l_d': convertToString,
                'cnc': convertToString
            }
        )

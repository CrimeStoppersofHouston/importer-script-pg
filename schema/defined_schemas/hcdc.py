'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-29 10:51:54
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-29 15:38:21
 # @ Description:
        This file contains the assembled schema for
        the HCDC database.
 '''

### External Imports ###

import json
from contextlib import closing
from datetime import datetime

### Internal Imports ###

from schema.schema import Schema, Table, Column
from utility.conversionFunctions import convertSPN

### Variable Declarations ###

with closing(open('config/schemaConfig.json')) as f:
    hcdcConfig = json.load(f)['hcdc']

hcdcSchema = Schema(hcdcConfig['name'], hcdcConfig['server'], hcdcConfig['port']
    ).addTable(
        Table('case_type', '', False)
        .addColumn(Column('id', int, 'cdi'))
        .addColumn(Column('literal', str, ''))

    ).addTable(
        Table('offense', 'offense_stage')
        .addColumn(Column('id', str, 'curr_off'))
        .addColumn(Column('literal', str, 'curr_off_lit'))

    ).addTable(
        Table('case_status', '', False)
        .addColumn(Column('id', str, 'cst'))
        .addColumn(Column('literal', str, ''))

    ).addTable(
        Table('defendant_status', '', False)
        .addColumn(Column('id', str, 'dst'))
        .addColumn(Column('literal', str, ''))

    ).addTable(
        Table('attorney', 'attorney_stage')
        .addColumn(Column('spn', str, 'aty_spn', convertSPN))
        .addColumn(Column('name', str, 'aty_nam'))
        
    ).addTable(
        Table('disposition', '', False)
        .addColumn(Column('id', str, 'cad'))
        .addColumn(Column('literal', str, ''))

    ).addTable(
        Table('report', 'report_stage')
        .addColumn(Column('id', str, 'off_rpt_num'))
        .addColumn(Column('agency', str, 'comp_agency'))
        .addColumn(Column('name', str, 'comp_nam'))

    ).addTable(
        Table('defendant', 'defendant_stage')
        .addColumn(Column('spn', str, 'def_spn', convertSPN))
        .addColumn(Column('name', str, 'def_nam'))
        .addColumn(Column('race', str, 'def_rac'))
        .addColumn(Column('sex', str, 'def_sex'))
        .addColumn(Column('date_of_birth', datetime, 'def_dob'))
        .addColumn(Column('street_name', str, 'def_stnam'))
        .addColumn(Column('street_number', str, 'def_stnum'))
        .addColumn(Column('city', str, 'def_cty'))
        .addColumn(Column('state', str, 'def_st'))
        .addColumn(Column('zip_code', str, 'def_zip'))
        .addColumn(Column('citizen', str, 'def_citizen'))

    ).addTable(
        Table('case', 'case_stage')
        .addColumn(Column('id', int, 'cas'))
        .addColumn(Column('case_type_id', int, 'cdi'))
        .addColumn(Column('report_id', str, 'off_rpt_num'))
        .addColumn(Column('offense_id', int, 'curr_off'))
        .addColumn(Column('defendant_spn', str, 'def_spn', convertSPN))
        .addColumn(Column('case_status_id', str, 'cst'))
        .addColumn(Column('defendant_status_id', str, 'dst'))
        .addColumn(Column('attorney_spn', str, 'aty_spn', convertSPN))
        .addColumn(Column('court', int, 'crt'))
        .addColumn(Column('filing_date', datetime, 'fda'))
    
    ).addTable(
        Table('event', 'event_stage')
        .addColumn(Column('case_id', int, 'cas'))
        .addColumn(Column('case_type_id', int, 'cdi'))
        .addColumn(Column('disposition', str, 'disposition'))
        .addColumn(Column('disposition_code', str, 'cad'))
        .addColumn(Column('sentence', str, 'sentence'))
        .addColumn(Column('disposition_date', datetime, 'dispdt'))
        .addColumn(Column('bond_explanation', str, 'bamexp'))
        .addColumn(Column('bond_amount', str, 'bam'))
    )
### External Imports ###

from datetime import datetime

### Internal Imports ###

from model.database.databaseModel import Table, Column, Schema

### Execution ###

database = Schema(
    'testing'
).addTable(
    Table(
        'offense'
    ).addColumn(
        Column('curr_off', 'id', int)
    ).addColumn(
        Column('curr_off_lit', 'literal', str)
    )
).addTable(
    Table(
        'attorney'
    ).addColumn(
        Column('aty_spn', 'spn', str)
    ).addColumn(
        Column('aty_nam', 'name', str)
    )
).addTable(
    Table(
        'report'
    ).addColumn(
        Column('off_rpt_num', 'id', str)
    ).addColumn(
        Column('comp_agency', 'agency', str)
    ).addColumn(
        Column('comp_nam', 'name', str)
    )
).addTable(
    Table(
        'defendant'
    ).addColumn(
        Column('def_spn', 'spn', str)
    ).addColumn(
        Column('def_nam', 'name', str)
    ).addColumn(
        Column('def_rac', 'race', str)
    ).addColumn(
        Column('def_sex', 'sex', str)
    ).addColumn(
        Column('def_dob', 'date_of_birth', str)
    ).addColumn(
        Column('def_stnum', 'street_number', str)
    ).addColumn(
        Column('def_stnam', 'street_name', str)
    ).addColumn(
        Column('def_cty', 'city', str)
    ).addColumn(
        Column('def_st', 'state', str)
    ).addColumn(
        Column('def_zip', 'zip_code', str)
    ).addColumn(
        Column('def_citizen', 'citizen', str)
    )
).addTable(
    Table(
        'event'
    ).addColumn(
        Column('cas', 'case_id', int)
    ).addColumn(
        Column('cdi', 'case_type_id', int)
    ).addColumn(
        Column('disposition', 'disposition', str)
    ).addColumn(
        Column('cad', 'disposition_code', str)
    ).addColumn(
        Column('sentence', 'sentence', str)
    ).addColumn(
        Column('dispdt', 'disposition_date', datetime)
    ).addColumn(
        Column('bamexp', 'bond_explanation', str)
    ).addColumn(
        Column('bam', 'bond_amount', str)
    )
)

cases = Table(
        'cases'
    ).addColumn(
        Column('cas', 'id', int)
    ).addColumn(
        Column('cdi', 'case_type_id', int)
    ).addColumn(
        Column('off_rpt_num', 'report_id', str)
    ).addColumn(
        Column('curr_off', 'offense_id', int)
    ).addColumn(
        Column('def_spn', 'defendant_spn', str)
    ).addColumn(
        Column('cst', 'case_status_id', str)
    ).addColumn(
        Column('dst', 'defendant_status_id', str)
    ).addColumn(
        Column('aty_spn', 'attorney_spn', str)
    ).addColumn(
        Column('crt', 'court', int)
    ).addColumn(
        Column('fda', 'filing_date', datetime)
    )

cases.addPrereq(database.getTablebyName('offense'))
cases.addPrereq(database.getTablebyName('attorney'))
cases.addPrereq(database.getTablebyName('defendant'))
cases.addPrereq(database.getTablebyName('event'))

database.addTable(cases)
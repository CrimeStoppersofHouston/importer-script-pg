'''
    Preset for the crime-index database
'''

### External Imports ###

from numpy import datetime64

### Internal Imports ###

from model.database.database_model import Table, Column, Schema
from automation.schema_creation import create_crime_index

database = Schema(
    'default', False, create_crime_index.create
).add_table(
    Table(
        'data'
    ).add_column(
        Column('Year', 'year', int, True)
    ).add_column(
        Column('Month', 'month', int, True)
    ).add_column(
        Column('Type', 'type', str, True)
    ).add_column(
        Column('Reporting Year', 'reportingYear', int, True)
    ).add_column(
        Column('Reporting Month', 'reportingMonth', int, True)
    ).add_column(
        Column('Category', 'category', str, True)
    ).add_column(
        Column('Count', 'count', int)
    )
)
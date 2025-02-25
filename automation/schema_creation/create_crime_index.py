'''
This module is meant to be used to create a new instance of the crime index database.
It includes a creation statement and a creation function for this purpose.
'''

### External Imports ###

import contextlib
import logging
import pyodbc

### Internal Imports ###

from utility.connection.connection_pool import ConnectionPool

### Variable Declarations ###

CREATE_STMT = """
create table if not exists data (
	year int,
    month int, 
    type varchar(20),
    reportingYear int,
    reportingMonth int,
    category varchar(50),
    count int,
    primary key (year, month, type, reportingYear, reportingMonth, category)
);
"""

def create(
    schema_name: str, connection: pyodbc.Connection, connection_pool: ConnectionPool
) -> None:
    '''Creates a new HCDC snapshot database with a predefined creation statement'''
    with contextlib.closing(connection.cursor()) as cursor:
        cursor.execute(f"create schema if not exists {schema_name}")
        cursor.commit()

        old_schema = connection_pool.schema
        connection_pool.set_schema(schema_name)
        new_connection = connection_pool.get_connection()
        new_cursor = new_connection.cursor()
        new_cursor.execute(f'set search_path to {schema_name}')
        for statement in CREATE_STMT.split(';'):
            if statement.strip() == '':
                continue
            try:
                new_cursor.execute(statement)
            except Exception as e:
                logging.error(e)
            
        new_cursor.commit()
        new_connection.close()

        connection_pool.set_schema(old_schema)
        connection_pool.free_connection(connection)
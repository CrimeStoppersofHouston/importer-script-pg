'''
This module is meant to be used to create a new instance of the hcdc database.
It includes a creation statement and a creation function for this purpose.
'''

### External Imports ###

import contextlib
import logging
import pyodbc

### Internal Imports ###

from utility.connection.connection_pool import ConnectionPool

### Variable Declarations ###

CREATE_STMT = '''
create table if not exists offense (
	code varchar(4) primary key not null,
    literal varchar(100) not null
);

create table if not exists incident (
	incident_id bigint not null,
    incident_date date not null,
    offense_code varchar(4) not null,
    offense_count int not null,
    beat varchar(10) null,
    premise varchar(255) null,
    street_number varchar(20) null,
    street_name varchar(255) null,
    street_type varchar(5) null,
    suffix varchar(1) null,
    city varchar(50) null,
    zip_code varchar(20) null,
    map_longitude real,
    map_latitude real,
    primary key (incident_id),
    foreign key (offense_code) references offense(code)
);
'''

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
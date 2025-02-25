'''
    This module contains the functions needed to handle pyodbc connection cursor
    actions including insertion and merging of data into the database
'''

### External Imports ###

import logging
from contextlib import closing

import pandas as pd
import pyodbc

### Internal Imports ###

from model.database.database_model import Schema, Table
from utility.connection.connection_pool import ConnectionPool
from utility.conversion_functions import convert_to_sql
from utility.progress_tracking import ProgressTracker, Task

### Function Declarations ###

def execute_sql(cursor: pyodbc.Cursor, sql: str, max_retries: int = 5, attempt: int = 0, e_message = None):
    '''
        Executes a SQL statement using the given cursor and retries on fail 
        until maximum retries are reached.
    '''
    if attempt > max_retries:
        logging.debug('SQL Failed! %s', e_message)
        logging.debug('SQL statement failed!: %s', sql)
        raise RecursionError('Maximum retries reached for SQL statement')
    else:
        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as e:
            execute_sql(cursor, sql, max_retries, attempt+1, e)


def get_max(cursor: pyodbc.Cursor, schema: str, table: str, column: str):
    '''Gets the max value of the given column'''
    query = f'select max({column}) from {schema}.{table}'
    execute_sql(cursor, query)
    value = cursor.fetchall()[0][0]
    return int(value if value is not None else 0)

def get_min(cursor: pyodbc.Cursor, schema: str, table: str, column: str):
    '''Gets the min value of the given column'''
    query = f'select min({column}) from {schema}.{table}'
    execute_sql(cursor, query)
    value = cursor.fetchall()[0][0]
    return int(value if value is not None else 0)

def reset_stage_table(cursor:pyodbc.Cursor, schema: Schema, table: Table) -> None:
    '''
        Clears a table's data by dropping and remaking it. This should
        only be done with a prep table as it will not retain foreign relationships
    '''
    logging.debug('Resetting stage table: %s', table.name)
    execute_sql(cursor,
        f'truncate table stage_{table.name}'
    )
    execute_sql(cursor, f'alter sequence stage_{table.name}_entry_seq restart with 1')
    cursor.commit()
    logging.debug('stage_%s cleared!', table.name)


def insert_to_stage_table(
    connection_pool: ConnectionPool,
    connection: pyodbc.Connection,
    df: pd.DataFrame,
    schema: Schema,
    table: Table,
    tracker: ProgressTracker,
    limit = 1000
) -> None:
    '''
        Inserts data from a dataframe given a connection object, a schema, 
        and the stage table to insert into. 
        Intended to work with the ConnectionPool object. Frees connection at
        the end of execution.
    '''
    total_rows = len(df)
    table_task = Task(f'stage_{table.name}', total_rows)
    tracker.add_task(table_task)
    columns = [column for column in table.columns]
    column_keys = [column.name for column in columns]
    table_keys = [column.name for column in table.keys]
    sql = f'INSERT INTO stage_{table.name} ({','.join(column_keys)}) VALUES '

    with closing(connection_pool.get_cursor(connection)) as cursor:
        reset_stage_table(cursor, schema, table)
        rows = []
        for index, row in df.iterrows():
            if index % limit == 0 and index != 0:
                if len(rows) != 0:
                    execute_sql(
                        cursor,
                        (f'{sql}{','.join(rows)} ON CONFLICT ({','.join(table_keys)}) DO NOTHING;')
                    )
                    table_task.set_progress(index+1)
                    tracker.update()
                rows = []
            insert = [row[col.raw_name] for col in columns]
            if any(insert):
                sql_string = convert_to_sql(insert)
                rows.append(sql_string)
        if len(rows) != 0:
            execute_sql(
                cursor,
                (f'{sql}{','.join(rows)} ON CONFLICT ({','.join(table_keys)}) DO NOTHING;')
            )
            table_task.set_progress(total_rows)
            tracker.update()
        cursor.commit()
        schema.advance_table_state(table)
        connection_pool.free_connection(connection)

def merge_from_stage_table(
    connection_pool: ConnectionPool,
    connection: pyodbc.Connection,
    schema: Schema,
    table: Table,
    tracker: ProgressTracker,
    limit = 1000
):
    '''Inserts data from staging table to final table'''

    table_keys = [column.name for column in table.keys]
    with closing(connection_pool.get_cursor(connection)) as cursor:
        minimum = get_min(cursor, schema.name, f'stage_{table.name}', 'entry')
        maximum = get_max(cursor, schema.name, f'stage_{table.name}', 'entry')
        total_rows = maximum-minimum

        table_task = Task(table.name, total_rows//limit+2)
        tracker.add_task(table_task)
        columns = [column.name for column in table.columns]
        pairs = [
            f'{table.name}.{column} '
            f'= stage_{table.name}.{column}'
            for column in columns
        ]

        for i in range(total_rows//limit+2):
            sql = f'''
                INSERT INTO {table.name} ({','.join(columns)})
                SELECT {','.join(columns)} FROM stage_{table.name}
                WHERE entry >= {i*limit} and entry < {(i+1)*limit}
                ON CONFLICT ({','.join(table_keys)}) DO NOTHING
            '''
            execute_sql(cursor, sql)
            table_task.set_progress(i)
            tracker.update()
        table_task.set_progress(total_rows//limit+2)
        cursor.commit()
        schema.advance_table_state(table)
        connection_pool.free_connection(connection)

def insert_to_table(
    connection_pool: ConnectionPool,
    connection: pyodbc.Connection,
    df: pd.DataFrame,
    schema: Schema,
    table: Table,
    tracker: ProgressTracker,
    limit = 1000
):
    '''
        Inserts data from a dataframe given a connection object, a schema, 
        and the table to insert into. 
        Intended to work with the ConnectionPool object. Frees connection at
        the end of execution.
    '''
    total_rows = len(df)
    table_task = Task(f'{table.name}', total_rows)
    tracker.add_task(table_task)
    columns = [column for column in table.columns]
    column_keys = [column.name for column in columns]
    table_keys = [column.name for column in table.keys]
    sql = f'INSERT INTO {table.name} ({','.join(column_keys)}) VALUES '

    with closing(connection_pool.get_cursor(connection)) as cursor:
        rows = []
        for index, row in df.iterrows():
            if index % limit == 0 and index != 0:
                if len(rows) != 0:
                    execute_sql(
                        cursor,
                        (f'{sql}{','.join(rows)} ON CONFLICT on constraint {table.name}_pkey DO NOTHING;')
                    )
                    table_task.set_progress(index+1)
                    tracker.update()
                rows = []
            insert = [row[col.raw_name] for col in columns]
            if any(insert):
                sql_string = convert_to_sql(insert)
                rows.append(sql_string)
        if len(rows) != 0:
            execute_sql(
                cursor,
                (f'{sql}{','.join(rows)} ON CONFLICT on constraint {table.name}_pkey DO NOTHING;')
            )
            table_task.set_progress(total_rows)
            tracker.update()
        logging.debug('Insertion completed! advancing table state')
        cursor.commit()
        schema.advance_table_state(table)
        connection_pool.free_connection(connection)

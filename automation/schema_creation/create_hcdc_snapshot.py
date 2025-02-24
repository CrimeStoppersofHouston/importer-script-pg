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
CREATE TABLE IF NOT EXISTS disposition (
  id varchar(4) NOT NULL,
  literal varchar(50) DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS case_status (
  id varchar(1) NOT NULL,
  literal varchar(50) DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS case_type (
  id smallint NOT NULL,
  literal varchar(15) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS defendant_status (
  id varchar(1) NOT NULL,
  literal varchar(50) DEFAULT NULL,
  PRIMARY KEY (id)
);

insert into disposition select * from lookup_tables.case_disposition on conflict do nothing;
insert into case_status select * from lookup_tables.case_status on conflict do nothing;
insert into case_type select * from lookup_tables.case_type on conflict do nothing;
insert into defendant_status select * from lookup_tables.defendant_status on conflict do nothing;

CREATE TABLE IF NOT EXISTS attorney (
  spn varchar(8) NOT NULL,
  name varchar(255) NOT NULL,
  PRIMARY KEY (spn)
);

CREATE TABLE IF NOT EXISTS defendant (
  spn varchar(8) NOT NULL,
  name varchar(255) DEFAULT NULL,
  race varchar(10) DEFAULT NULL,
  sex varchar(10) DEFAULT NULL,
  date_of_birth date DEFAULT NULL,
  street_number varchar(255) DEFAULT NULL,
  street_name varchar(255) DEFAULT NULL,
  city varchar(255) DEFAULT NULL,
  state varchar(10) DEFAULT NULL,
  zip varchar(10) DEFAULT NULL,
  citizen varchar(2) DEFAULT NULL,
  PRIMARY KEY (spn)
);

CREATE TABLE IF NOT EXISTS event (
  entry bigserial NOT NULL,
  case_id bigint NOT NULL,
  case_type_id smallint NOT NULL,
  disposition varchar(60) NOT NULL,
  disposition_code varchar(4) DEFAULT NULL,
  disposition_date date DEFAULT NULL,
  sentence varchar(60) DEFAULT NULL,
  bond_amount varchar(30) DEFAULT NULL,
  bond_explanation varchar(30) DEFAULT NULL,
  next_appearance date DEFAULT NULL,
  PRIMARY KEY (entry, case_id,case_type_id, disposition)
);

CREATE TABLE IF NOT EXISTS offense (
  id int NOT NULL,
  literal varchar(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS report (
  id varchar(25) NOT NULL,
  agency varchar(50) NOT NULL,
  name varchar(50) NOT NULL,
  PRIMARY KEY (id,agency,name)
);

CREATE TABLE IF NOT EXISTS cases (
  id bigint NOT NULL,
  case_type_id smallint NOT null references case_type(id),
  report_id varchar(25) DEFAULT null,
  offense_id int NOT null references offense(id),
  defendant_spn varchar(8) NOT null references defendant(spn),
  case_status_id varchar(1) DEFAULT null references case_status(id),
  defendant_status_id varchar(1) DEFAULT null references defendant_status(id),
  attorney_spn varchar(8) DEFAULT null references attorney(spn),
  court smallint DEFAULT NULL,
  filing_date date NOT NULL,
  PRIMARY KEY (id,case_type_id)
);

create index idx_cases_report_id on cases(report_id);
create index idx_cases_offense_id on cases(offense_id);
create index idx_cases_defendant_spn on cases(defendant_spn);
create index idx_cases_case_status_id on cases(case_status_id);
create index idx_cases_defendant_status_id on cases(defendant_status_id);
create index idx_cases_attorney_spn on cases(attorney_spn);

alter sequence event_entry_seq restart with 1;
insert into defendant (spn) values ('') on conflict do nothing;
insert into report (id, agency, name) values ('', '', '') on conflict do nothing;
insert into offense (id, literal) values (-1, 'NULL') on conflict do nothing;
insert into defendant_status (id, literal) values (1, 'Unknown') on conflict do nothing;
'''

### Function Declarations ###


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

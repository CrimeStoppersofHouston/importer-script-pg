'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-07-12 14:17:39
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-07-12 14:17:50
 # @ Description: 
        This file should contain the class needed to create,
        maintain, and remove connections with the mysql server
        in order to allow for multi-threaded inserts.
 '''

### External Imports ###

import pyodbc
import logging

### Class Declarations ###

class ConnectionPool:
    def __init__(self, username: str, password: str, server: str, port: int, database: str, driver: str, max_connections: int = 5):
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.database = database
        self.driver = driver

        self.pool = set()
        self.max_connections = max_connections


    def getConnection(self, maxRetries: int = 5) -> pyodbc.Connection:
        connection = None
        for tries in range(maxRetries):
            try:
                connection = pyodbc.connect(
                    f'Driver={self.driver};'
                    f'Server={self.server};'
                    f'Port={self.port}'
                    f'Database={self.database};'
                    f'Uid={self.username};'
                    f'Pwd={self.password};'
                    'Encrypt=yes;Connection Timeout=100;MULTI_HOST=1;', autocommit=False
                )
                logging.debug(f'Connection established on try {tries+1}')
            except Exception as e:
                logging.debug(f'Error getting connection: {e}')
        if connection is None:
            raise ConnectionError('Failed to establish connection to database')
        return connection
    
    def addConnection(self) -> pyodbc.Connection:
        if len(self.pool) >= self.max_connections:
            logging.error('Cannot add connection to pool, max connections has been reached!')
            return None
        connection = self.getConnection()
        self.pool.add(connection)
        return connection
    
    def removeConnection(self, connection: pyodbc.Connection) -> None:
        if connection not in self.pool:
            logging.error('Connection failed to be removed from pool: not present in pool')
            raise ValueError
        self.pool.remove(connection)
        connection.close()
        logging.debug('Connection successfully removed from pool')
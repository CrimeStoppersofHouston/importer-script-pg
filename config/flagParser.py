# This file contains the singleton instance of
# the flag parser. This is to avoid using multiple
# instances for the same program call.

### External Imports ###

import argparse

### Class Declarations ###

class FlagParser(argparse.ArgumentParser):
    # Singleton instance to avoid creating multiple instances
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(FlagParser, self).__new__(self)
        return self.instance
    
    def __init__(self):
        super().__init__(prog='python main.py',
                        description='This program is used to import historical HCDC files to a mysql database',
                        fromfile_prefix_chars='@')

        self.add_argument('-f', '--file', type=str, help='The filepath to load data from')
        self.add_argument('-d', '--directory', type=str, help='The directory to load data from (Will not search folders recursively)')
        self.add_argument('-s', '--schema', type=str, help='The schema name to import data into')
        self.add_argument('-debug', action='store_true', default=False, help='Enable debug mode')
        self.add_argument('-skipv', '--skipVerification', action='store_true', default=False, help='Skips the integrity checks for columns. (Recommended when importing multiple files)')
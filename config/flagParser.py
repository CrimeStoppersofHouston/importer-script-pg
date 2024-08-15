'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-20 15:40:12
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-29 15:45:03
 # @ Description: 
        This file contains the singleton instance of
        the flag parser. This is to avoid using multiple
        instances for the same program call.
 '''

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
                        description='This program is an import script for use in various CSOH mysql databases. Compatible with Python 3.11+',
                        fromfile_prefix_chars='@')
        fileGroup = self.add_mutually_exclusive_group(required=True)
        fileGroup.add_argument('-f', '--file', type=str, help='The filepath to load data from')
        fileGroup.add_argument('-d', '--directory', type=str, help='The directory to load data from (Will not search folders recursively)')
        fileGroup.add_argument('-hcdc', type=str, help='The directory to verify HCDC download files')
        
        self.add_argument('-c', '--collect', action='store_true', default=False, help='The extension to download HCDC datasets')
        self.add_argument('-e', '--extension', type=str, help='The extension to filter by when using the --directory argument')
        self.add_argument('-debug', action='store_true', default=False, help='Enable debug mode')
        self.add_argument('-skipv', '--skipVerification', action='store_true', default=False, help='Skips the integrity checks for columns. (Recommended when importing multiple files)')

        self.add_argument('-r', '--recursive', action='store_true', default=False, help='Enables recursion through subdirectories when using the --directory argument')
        self.add_argument('-depth', type=int, default=3, help='Depth of the recursion search when using the --directory argument with --recursive enabled. Defaults to 3.')

        self.add_argument('-delimiter', type=str, default=',', help='Delimiter for text files. Defaults to ",".')

        self.add_argument('-type', type=str, help='Specifies the type of file to use. (HCDC, etc.)', required=True)

        self.args = self.parse_args()

        if self.args.directory and self.args.extension is None:
            self.error('--directory requires --extension argument')

        if self.args.depth and self.args.recursive is None:
            self.error('-depth requires --recursive argument')

        if self.args.recursive and self.args.directory is None:
            self.error('--recursive requires --directory argument')
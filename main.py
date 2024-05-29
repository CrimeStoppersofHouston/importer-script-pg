'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-20 13:53:12
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-29 16:24:05
 # @ Description: 
        This is the main entrypoint for this program.
        Very little scripting should be included in this file, 
        all functions and objects should be referenced from other
        locations. This file will contain the main workflow of the
        program, and will maintain a small number of established variables.
 '''

### External Imports ###



### Internal Imports ###

from config.flagParser import FlagParser
from schema.defined_schemas.hcdc import hcdcSchema
from utility.fileFetching import fetchFromDirectory

### Variable Declarations ###

models = []

workflow = {
    'staging_tables':[],
    'final_tables':[]
}

### File Gathering ###



### Execution ###

print(fetchFromDirectory(FlagParser().args.directory, FlagParser().args.extension, True))

FlagParser().print_help()

print(hcdcSchema.name)
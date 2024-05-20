# This is the main entrypoint for this program.
# Very little scripting should be included in this file, 
# all functions and objects should be referenced from other
# locations. This file will contain the main workflow of the
# program, and will maintain a small number of established variables.

### External Imports ###



### Internal Imports ###

from config.flagParser import FlagParser

### Variable Declarations ###

models = []

workflow = {
    'staging_tables':[],
    'final_tables':[]
}

### File Gathering ###



### Execution ###

FlagParser().print_help()
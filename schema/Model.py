# This file contains the base model class declarations
# used to create a full schema. This should allow for
# the compilation of table and column names, as well as
# their data types and conversion functions.

### Class Declarations ###

def Model(object):
    def __init__(self, stage: str, fina: str, ):
        self.stage = ''
        self.final = ''

        self.columns = {}

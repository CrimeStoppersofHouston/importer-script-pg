# This file contains the base model class declarations
# used to create a full schema. This should allow for
# the compilation of table and column names, as well as
# their data types and conversion functions.

### Class Declarations ###

def Table():
    def __init__(self, stage: str, fina: str, ):
        self.stage = ''
        self.final = ''

        self.columns = {}

    def addColumn(self, name: str, datatype: type, conversionFunction: function = False):
        self.columns[name] = Column(name, datatype, )

def Column():
    def __init__(self, name: str, datatype: type, conversionFunction: function):
        self.name = name
        self.datatype = datatype
        self.conversionFunction = conversionFunction
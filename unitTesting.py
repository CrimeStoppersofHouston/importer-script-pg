'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-06-20 10:18:23
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-06-20 10:19:13
 # @ Description: 
    This file is meant to execute all unittests contained within 
    this directory and its subdirectories
 '''

### Internal Imports ###

from tests.testState import TestStateHolders
from tests.testFileFunctions import TestFileFunctions
from tests.testConnection import TestConnection

### External Imports ###

import unittest
import logging
from datetime import datetime

### Execution ###

logging.basicConfig(
   level=logging.DEBUG,
   format='%(asctime)s\t[%(levelname)s]\t%(message)s',
   handlers=[
         logging.FileHandler(f"./logs/{datetime.now().strftime('testing_debug_%Y%m%d_%H%M')}.log"),
   ]
)
unittest.main()
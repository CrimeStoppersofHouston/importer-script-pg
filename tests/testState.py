'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-06-20 10:30:24
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-06-21 10:25:05
 # @ Description: 
    Tests for state classes which control program execution
 '''

import unittest

from config.states import *


class TestStateHolders(unittest.TestCase):
    def setUp(self):
        self.fstate = FileState()
        self.pstate = ProgramState()

    def testSetGetState(self):
        self.fstate.setState(FileStates.END)
        self.assertEqual(self.fstate.getState(), FileStates.END)

        self.pstate.setState(ProgramStates.END)
        self.assertEqual(self.pstate.getState(), ProgramStates.END)

    def testStateExclusivity(self):
        try:
            self.fstate.setState(ProgramStates.END)
            self.assertEqual(1, 0, "File state exclusivity violated!")
        except Exception as e:
            self.assertIsInstance(e, ValueError)
        
        try:
            self.pstate.setState(FileStates.END)
            self.assertEqual(1, 0, "Program state exclusivity violated!")
        except Exception as e:
            self.assertIsInstance(e, ValueError)
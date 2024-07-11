'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-06-20 13:54:42
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-06-21 10:25:38
 # @ Description: 
    Tests for file fetching functions
 '''

import unittest
import os

from utility.file.filefetch import fetchFromDirectory
from utility.file.filevalidate import validateFromModel
from utility.file.fileload import loadDataframeTSV
from model.fileModel import HCDCModel

class TestFileFunctions(unittest.TestCase):
    def setUp(self):
        pass

    ### File Fetching ###

    def testGetDirectorySingle(self):
        files = set([os.path.basename(x) for x in fetchFromDirectory('./tests/testSetups/directorySearch', '.txt')])
        expected = set(['1.txt'])

        self.assertEqual(files, expected)

    def testGetDirectoryOneDepth(self):
        files = set([os.path.basename(x) for x in fetchFromDirectory('./tests/testSetups/directorySearch', '.txt', True, 1)])
        expected = set(['1.txt', '2.txt', '3.txt', '4.txt', '6.txt'])

        self.assertEqual(files, expected)

    def testGetDirectoryTenDepth(self):
        files = set([os.path.basename(x) for x in fetchFromDirectory('./tests/testSetups/directorySearch', '.txt', True, 10)])
        expected = set(['1.txt', '2.txt', '3.txt', '4.txt', '6.txt', '9.txt', '10.txt'])

        self.assertEqual(files, expected)

    def testExtensionAdherence(self):
        files = set([os.path.basename(x) for x in fetchFromDirectory('./tests/testSetups/directorySearch', '.pdf')])
        expected = set(['document.pdf'])

        self.assertEqual(files, expected)
    
    @unittest.expectedFailure
    def testNegativeDepthFail(self):
        fetchFromDirectory('./tests/testSetups/directorySearch', '.pdf', True, -1)

    ### File Validation ###

    def testHCDCValidation(self):
        df = loadDataframeTSV('./tests/testSetups/sampleFile/HCDC_sample_chunk.txt')
        self.assertTrue(validateFromModel(df, HCDCModel()))
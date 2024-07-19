'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-29 15:48:01
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-30 12:14:30
 # @ Description: 
        This file contains all of the functions needed to fetch file names
        for use in the main execution of the program.
 '''

### External Imports ###

import os
import glob
from datetime import date
import logging

### Function Declarations ###

def fetchFromDirectory(directoryPath: str, extension: str, recursive: bool = False, depthLimit: int = 3, depth: int = 0) -> list[str]:
    if depthLimit < 0:
        raise ValueError("Depth limit for directory fetch must not be less than 0!")

    fileList = []
    if not os.path.exists(directoryPath):
        raise ValueError(f'Directory does not exist: {directoryPath}')

    # Recursion with depth limit 
    if recursive and depth < depthLimit:
        subDirectories = [f'{directoryPath}\\{d}' for d in os.listdir(directoryPath) if os.path.isdir(f'{directoryPath}\\{d}')]
        for directory in subDirectories:
            fileList += fetchFromDirectory(directory, extension, recursive, depthLimit, depth+1)

    # Fetching file paths
    for f in os.listdir(directoryPath):
        if f.endswith(extension):
            fileList.append(f'{directoryPath}\\{f}')
    
    return fileList

def hcdcFileValidation(directoryPath: str):
    todays_date = date.today()
    filepaths = []
    code = 0
    fileList, status = dailyFilingsCheck(directoryPath, todays_date)
    filepaths += fileList
    code += status
    fileList, status = monthlyFilingsCheck(directoryPath, todays_date)
    filepaths += fileList
    code += status
    fileList, status = historicalFilingsCheck(directoryPath, todays_date)
    filepaths += fileList
    code += status
    codeCheck(code)
    
    return filepaths, code
    # print (type(todays_date))
    # return fileList
    
def dailyFilingsCheck(directoryPath: str, date: date):
    fileList = glob.glob(f'{directoryPath}\\{date.year}-{date.month:02d}-*[0-9] CrimFilingsDaily_withHeadings.txt')
    status = 0
    if len(fileList) == date.day:
        status = 1
    return fileList, status

def monthlyFilingsCheck(directoryPath: str, date: date):
    fileList = glob.glob(f'{directoryPath}\\{date.year}-{date.month:02d}-*[0-9] CrimFilingsMonthly_withHeadings.txt')
    status = 0
    if len(fileList):
        status = 2
    return fileList, status
    
def historicalFilingsCheck(directoryPath: str, date: date):
    fileList = glob.glob(f'{directoryPath}\\Weekly_Historical_Criminal_{date.year}{date.month:02d}*[0-9].txt')
    status = 0
    if len(fileList):
        status = 4
    return fileList, status

def codeCheck(code: int):
    match code:
        case 0:
            logging.info("No HCDC files found")
        case 1:
            logging.info("MISSING FILES: Monthly Filings, Historical Files")
        case 2:
            logging.info("MISSING FILES: Daily Filings, Historical Filings")
        case 3:
            logging.info("MISSING FILES: Historical Files")
        case 4:
            logging.info("MISSING FILES: Daily Filings, Monthly Filings")
        case 5:
            logging.info("MISSING FILES: Monthly Filings")
        case 6:
            logging.info("MISSING FILES: Daily Filings")
        case 7:
            logging.info("All HCDC files found") 
            
    
    
# historicalFilingsCheck("D:\CrimeStoppers\HCDC-data-fetch\hcdc-importer\data", date.today())
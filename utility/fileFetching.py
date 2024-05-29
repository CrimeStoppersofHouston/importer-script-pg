'''
 # @ Author: Ryan Barnes
 # @ Create Time: 2024-05-29 15:48:01
 # @ Modified by: Ryan Barnes
 # @ Modified time: 2024-05-29 16:23:53
 # @ Description: 
        This file contains all of the functions needed to fetch file names
        for use in the main execution of the program.
 '''

### External Imports ###

import os

### Function Declarations ###

def fetchFromDirectory(directoryPath: str, extension: str, recursive: bool = False, depth: int = 0, depthLimit: int = 3) -> list[str]:
    fileList = []
    if not os.path.exists(directoryPath):
        raise ValueError(f'Directory does not exist: {directoryPath}')

    # Recursion with depth limit 
    if recursive and depth < depthLimit:
        subDirectories = [f'{directoryPath}\\{d}' for d in os.listdir(directoryPath) if os.path.isdir(f'{directoryPath}\\{d}')]
        for directory in subDirectories:
            fileList += fetchFromDirectory(directory, extension, recursive, depth+1, depthLimit)

    # Fetching file paths
    for f in os.listdir(directoryPath):
        if f.endswith(extension):
            fileList.append(f'{directoryPath}\\{f}')

    return fileList
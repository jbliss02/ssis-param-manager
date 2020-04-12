import os
import configparser

seed = 'C:/Users/james/source/repos/ssis_digitex'
dirs = []
files = []

def Go():

    dirs.append(seed)
    
    while len(dirs) > 0:
        ScanDir(dirs[0])

    test = 'sss'

def ScanDir(dir):

    with os.scandir(dir) as entries:
        dirs.remove(dir)
        for entry in entries:
            if entry.is_file() and entry.name.endswith('dtsx'):
                files.append(entry)
            elif entry.is_dir() and not entry.name.startswith('.'):
                dirs.append(dir + '/' + entry.name)

Go()
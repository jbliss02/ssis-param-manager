import os
import configparser
import xmltodict
from dtsx import DTSXFile

seed = 'C:/Users/james/source/repos/ssis_digitex'
dirs = []
files = []
dtsx = []

def GetFiles():

    dirs.append(seed)
    
    while len(dirs) > 0:
        ScanDir(dirs[0])

def ScanDir(dir):

    with os.scandir(dir) as entries:
        dirs.remove(dir)
        for entry in entries:
            AnalyseFolderItem(entry, dir)

def AnalyseFolderItem(entry, dir):

    if entry.is_file() and entry.name.endswith('dtsx'):
        files.append(entry)
    elif entry.is_dir() and not entry.name.startswith('.'):
        dirs.append(dir + '/' + entry.name)

def ExtractParamsFromFiles():

    for file in files:
        with open(file.path, encoding='utf-8-sig') as fd:
            xml = xmltodict.parse(fd.read())
            CreateSummary(file, xml)

def CreateSummary(file, xml):

    summary = DTSXFile()
    summary.fileInfo = file

    dtsx.append(summary)
    con = GetConnectionInfo(xml)
    x = 11

def GetConnectionInfo(xml):
    
    result = []

    for conInfo in xml['DTS:Executable']['DTS:ConnectionManagers']['DTS:ConnectionManager']:
        result.append(conInfo)

    return result

GetFiles()
ExtractParamsFromFiles()

t = 1
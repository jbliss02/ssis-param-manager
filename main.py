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
    AddConnectionInfo(summary, xml)

    dtsx.append(summary)
    x = 11

def AddConnectionInfo(file, xml):
    
    result = []

    if not 'DTS:ConnectionManagers' in xml['DTS:Executable']:
        return

    for conInfo in xml['DTS:Executable']['DTS:ConnectionManagers']['DTS:ConnectionManager']:

        if not 'DTS:ObjectData' in conInfo or not isinstance(conInfo, dict):
            continue

        if 'DTS:ConnectionManager' in conInfo['DTS:ObjectData'] and '@DTS:ConnectionString' in conInfo['DTS:ObjectData']['DTS:ConnectionManager']:

            if not conInfo['DTS:ObjectData']['DTS:ConnectionManager']['@DTS:ConnectionString'] in file.connnectionInfo:
                file.connnectionInfo.append(conInfo['DTS:ObjectData']['DTS:ConnectionManager']['@DTS:ConnectionString'])

        elif 'SmtpConnectionManager' in conInfo['DTS:ObjectData']:

            if not conInfo['DTS:ObjectData']['SmtpConnectionManager']['@ConnectionString'] in file.connnectionInfo:
                file.connnectionInfo.append(conInfo['DTS:ObjectData']['SmtpConnectionManager']['@ConnectionString'])

    return result

GetFiles()
ExtractParamsFromFiles()

t = 1
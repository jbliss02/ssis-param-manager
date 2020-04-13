import os
import configparser
import xmltodict
import configparser
from dtsx import DTSXFile
from dtsx import DTSXParameter

config = configparser.ConfigParser()
config.read("config.ini")
seed = config.get('IO', 'seedDirectory')

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
    AddParameters(summary, xml)
    dtsx.append(summary)

def AddConnectionInfo(file, xml):
    
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

def AddParameters(file, xml):

    if not 'DTS:PackageParameters' in xml['DTS:Executable']:
        return

    params = []

    for item in xml['DTS:Executable']['DTS:PackageParameters']['DTS:PackageParameter']:

        if not isinstance(item, dict) or not '#text' in item['DTS:Property']:
            continue

        param = DTSXParameter()
        param.name = item['@DTS:ObjectName']
        param.value = item['DTS:Property']['#text']

        params.append(param)

    if (len(params) > 0):
        file.parameters.append(params)

GetFiles()
ExtractParamsFromFiles()

t = 1
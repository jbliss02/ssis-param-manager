import csv
import os
import configparser
import xmltodict
import configparser
import extraction
from dtsx import DTSXFile
from dtsx import DTSXParameter

config = configparser.ConfigParser()
config.read("config.ini")

dirs = []
files = []
dtsx = []

def GetFiles():

    seeds = config.items('SeedDirectories')

    for key, seed in seeds:
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
    summary.connectionInfo = []
    summary.parameters = []
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

            if not conInfo['DTS:ObjectData']['DTS:ConnectionManager']['@DTS:ConnectionString'] in file.connectionInfo:
                file.connectionInfo.append(conInfo['DTS:ObjectData']['DTS:ConnectionManager']['@DTS:ConnectionString'])

        elif 'SmtpConnectionManager' in conInfo['DTS:ObjectData']:

            if not conInfo['DTS:ObjectData']['SmtpConnectionManager']['@ConnectionString'] in file.connectionInfo:
                file.connectionInfo.append(conInfo['DTS:ObjectData']['SmtpConnectionManager']['@ConnectionString'])

def AddParameters(file, xml):

    if not 'DTS:PackageParameters' in xml['DTS:Executable']:
        return

    for item in xml['DTS:Executable']['DTS:PackageParameters']['DTS:PackageParameter']:

        if not isinstance(item, dict) or not '#text' in item['DTS:Property']:
            continue

        param = DTSXParameter()
        param.name = item['@DTS:ObjectName']
        param.value = item['DTS:Property']['#text'].replace('\u200b', '')

        file.parameters.append(param)

def WriteToCSV():

    f = open(config.get('IO', 'outputFile'), 'w', newline='')

    with f:

        writer = csv.writer(f)
        
        for file in dtsx:
            for connection in file.connectionInfo:
                writer.writerow([file.fileInfo.name, 'ConnectionString', connection])
            for param in file.parameters:
                writer.writerow([file.fileInfo.name, param.name, param.value])

GetFiles()
ExtractParamsFromFiles()
extraction.ExtractPaths(dtsx, True)
#WriteToCSV()
import csv
from locationMapping import LocationMapping 

filePaths = []
serverLocationMapping = []

def WriteServerLocationsToFile(dtsx, removeServerName, removeDrives, resultsFilePath):

    ExtractPaths(dtsx, removeServerName, removeDrives)

    f = open(resultsFilePath, 'w', newline='')

    with f:
        writer = csv.writer(f)

        writer.writerow(['Original', 'FileName', 'New'])

        for mapping in serverLocationMapping:
            writer.writerow([mapping.original, mapping.fileName, mapping.new])
            
def ExtractPaths(dtsx, removeServerName, removeDrives):

    for file in dtsx:
        for connection in file.connectionInfo:
            if IsPath(connection):
                Add(connection, removeServerName, removeDrives)
        for param in file.parameters:
            if IsPath(param.value):
                Add(param.value, removeServerName, removeDrives)


def Add(value, removeServerName, removeDrives):

    serverLocationMapping.append(AddFile(value, removeServerName, removeDrives))

def AddFile(value, removeServerName, removeDrives):
    
    result = LocationMapping()
    result.original = value

    split = value.split('\\')

    #remove the blanks
    while ('' in split):
        split.remove('')

    #are there any files
    for item in split:
        if '.' in item:
            x = 2

    #add to the list of files if it is a file
    if '.' in split[len(split) - 1]:
        filePaths.append(value)
        result.fileName = split[len(split) - 1]
        split.remove(result.fileName)

    if removeServerName:
        split.remove(split[0])

    if removeDrives:
        for item in split:
            if '$' in item:
                split.remove(item)
                continue

    for item in split:

        if len(item) > 0:
            result.new += '\\\\' + item

    return result

def IsPath(value):
    return value.startswith('\\\\')





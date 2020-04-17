filePaths = []
serverLocations = []

def ExtractPaths(dtsx, removeServerName):

    for file in dtsx:
        for connection in file.connectionInfo:
            if IsPath(connection):
                Add(connection, removeServerName)
        for param in file.parameters:
            if IsPath(param.value):
                Add(param.value, removeServerName)

    serverLocations.sort()
    filePaths.sort()

    return 1

def Add(value, removeServerName):

    value = AddFile(value, removeServerName)

    if not value in serverLocations:
        serverLocations.append(value)

def AddFile(value, removeServerName):
    
    split = value.split('\\')

    while ('' in split):
        split.remove('')

    if len(split) < 2:
        return value

    if '.' in split[len(split) - 1] and not value in filePaths:
        filePaths.append(value)

    split.remove(split[len(split) - 1])

    if removeServerName:
        split.remove(split[0])

    result = ''

    for item in split:

        if len(item) > 0:
            result += '\\\\' + item

    return result


def IsPath(value):
    return value.startswith('\\\\')





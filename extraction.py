filePaths = []

def ExtractServerPaths(dtsx):

    for file in dtsx:
        for connection in file.connectionInfo:
            if connection.startswith('\\\\'):
                AddToFilePath(connection)
        for param in file.parameters:
            if param.value.startswith('\\\\'):
                AddToFilePath(param.value)

    return filePaths

def AddToFilePath(value):

    if not value in filePaths:
        filePaths.append(value)

def ExtractServerPaths(dtsxFiles):

    result = []

    for file in dtsx:
        for connection in file.connectionInfo:
            if connection.startswith.('\\\\'):
                result.append(connection)
        for param in file.parameters:
            if param.value.startswith('\\\\'):
                result.append(connection)

import os
import configparser

seed = 'C:/Users/james/source/repos/ssis_digitex'

dirs = []
dirs.append(seed)

files = []

with os.scandir(seed) as entries:
    for entry in entries:
        if entry.is_file() and entry.name.endswith('dtsx'):
            files.append(entry)
        elif entry.is_dir() and not entry.name.startswith('.'):
            dirs.append(entry)

test = 'sss'

# config = configparser.ConfigParser()
# config.read("config/config.ini")
# saveDirectory = config.get('IO', 'tempDirectory')

# def FootballDataUrl():
#     return config.get('FootballData', 'dataUrl')


# def FileNames():
#     result = []
#     file = open(config.get('FootballData', 'divisionFileNames'))

#     for line in file:
#         result.append(line.strip() + ".csv")

#     return result

# def CreateDirectoryIfNotExists(directory):
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# def SeasonCode(initialYear):
#     return str(initialYear)[2:4] + str(initialYear + 1)[2:4]

# def CurrentSeason():
#     now = datetime.datetime.now()
#     if(now.month > 6):
#         return SeasonCode(now.year)
#     else:
#         return SeasonCode(now.year - 1)

# def DownloadAllDataFiles():
#     startingYear = int(config.get('GetAllData', 'startYear'))

#     for year in YearArray(startingYear):
#         DownloadSeason(year)

# def DownloadCurrentSeasonFiles():
#     DownloadSeason(CurrentSeason())

# def DownloadSeason(season):
#     for file in FileNames():
#         downloadUrl = FootballDataUrl() + "/" + season + "/" + file
#         savePath = saveDirectory + season

#         CreateDirectoryIfNotExists(savePath)
#         TryDownload(downloadUrl, savePath + "/" + file)

# def TryDownload(downloadUrl, savePath):
#     sleepSeconds = int(config.get('FootballData', 'downloadDelaySeconds'))

#     #not all files will exist (coverage of conference for example doesn't appear in earlier files) hence the catch
#     try:
#         print("Trying to download: " + downloadUrl)
#         urllib.request.urlretrieve(downloadUrl, savePath)
#         time.sleep(sleepSeconds)
#     except Exception:
#         pass


# #Run from here
# #DownloadCurrentSeasonFiles()

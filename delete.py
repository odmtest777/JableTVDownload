import os

def deleteMp4(folderPath):
    files = os.listdir(folderPath)
    for file in files:
        if "index" in file:
            os.remove(os.path.join(folderPath, file))


def deleteM3u8(folderPath):
    files = os.listdir(folderPath)
    for file in files:
        if file.endswith('.m3u8'):
            os.remove(os.path.join(folderPath, file))

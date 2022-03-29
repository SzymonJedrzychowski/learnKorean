from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json


def load(lastFileTime: int):
    """Load file from the google drive
    
    :param lastFileTime: time of last save of save file
    """

    gauth = GoogleAuth("data/json/settings.yaml")
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file = drive.CreateFile({"id": "1-XFgSplPR3imq2DfH_opeaxpmM4W-ct7"})
    thisFileTime = json.loads(file.GetContentString())["time"]

    if thisFileTime < lastFileTime:
        return [False, 0]
    elif thisFileTime == lastFileTime:
        return [False, 1]

    file.GetContentFile("data/json/data.json")

    return [True]


def save():
    """Save data to the google drive"""

    gauth = GoogleAuth("data/json/settings.yaml")
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file = drive.CreateFile({"id": "1-XFgSplPR3imq2DfH_opeaxpmM4W-ct7"})
    file.SetContentFile("data/json/data.json")
    file.Upload()

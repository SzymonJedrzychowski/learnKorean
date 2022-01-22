import io
import os
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from pathlib import Path


def load(lastFileTime: int):
    """Load file from the google drive

    :param lastFileTime: time of last save of save file
    """
    creds = None

    dataPath = str(
        Path("fileOperations.py").absolute().parents[0])+"/data/json/"

    if os.path.exists('{}token.json'.format(dataPath)):
        creds = Credentials.from_authorized_user_file('{}token.json'.format(
            dataPath), ['https://www.googleapis.com/auth/drive'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '{}credentials.json'.format(dataPath), ['https://www.googleapis.com/auth/drive'])
            creds = flow.run_local_server(port=0)

        with open('{}token.json'.format(dataPath), 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    thisFileTime = int(service.files().get(
        fileId='1-XFgSplPR3imq2DfH_opeaxpmM4W-ct7', fields="description").execute()["description"])

    if thisFileTime < lastFileTime:
        return [False, 1]
    elif thisFileTime == lastFileTime:
        return [False, 1]

    request = service.files().get_media(fileId='1-XFgSplPR3imq2DfH_opeaxpmM4W-ct7')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    with open("{}data.json".format(dataPath), "wb") as f:
        f.write(fh.getbuffer())

    return [True]


def save():
    """Save data to the google drive"""

    currentTime = int(time.time())
    creds = None

    dataPath = str(
        Path("fileOperations.py").absolute().parents[0])+"/data/json/"

    if os.path.exists('{}token.json'.format(dataPath)):
        creds = Credentials.from_authorized_user_file('{}token.json'.format(
            dataPath), ['https://www.googleapis.com/auth/drive'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '{}credentials.json'.format(dataPath), ['https://www.googleapis.com/auth/drive'])
            creds = flow.run_local_server(port=0)

        with open('{}token.json'.format(dataPath), 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    media = MediaFileUpload('{}data.json'.format(dataPath),
                            mimetype='text/json',
                            resumable=True)
    file = service.files().update(fileId='1-XFgSplPR3imq2DfH_opeaxpmM4W-ct7',
                                  media_body=media, body={"description": currentTime}).execute()

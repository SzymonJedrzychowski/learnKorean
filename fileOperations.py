from fileOperations import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import os

def load(lastFileTime):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/drive'])
            creds = flow.run_local_server(port=0)
    
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, description)").execute()
    items = results.get('files', [])

    thisFileTime = 0
    for item in items:
        if item["name"] == "data.json":
            thisFileTime = int(item["description"])

    if thisFileTime<lastFileTime:
        return False
    elif thisFileTime==lastFileTime:
        return True

    request = service.files().get_media(fileId='1-XFgSplPR3imq2DfH_opeaxpmM4W-ct7')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    with open("data.json", "wb") as f:
        f.write(fh.getbuffer())

def save(currentTime):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/drive'])
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    media = MediaFileUpload('data.json',
                            mimetype='text/json',
                            resumable=True)
    file = service.files().update(fileId='1-XFgSplPR3imq2DfH_opeaxpmM4W-ct7', media_body = media, body = {"description": currentTime}).execute()
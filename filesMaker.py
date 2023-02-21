from __future__ import print_function
import httplib2
import os, io

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None
import auth

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
#print(authInst)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
#print(http)
drive_service = discovery.build('drive', 'v3', http=http)

def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))

def copyNancyCasual(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '17mPHaOvx3Ia-PKZcCyIsxgzn5Ww9KHl9y5BCXgwRmww',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document',
                    'iconLink':'https://drive-thirdparty.googleusercontent.com/16/type/application/vnd.google-apps.document',
                    'fileId': file.get('id')
                    }
    t = [attachment1]
    return t

def copyNancyCorp(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '1JhjgiKvJI2outSKyvrU6KkRtEWK5NczXEWEpJ7czEW0',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()

    sheet = drive_service.files().copy(body = file_metadata,
                                      fileId = '1mChCvb26iWC2TFSs6SMWLswcwTzoltEq6aI4IFLY4mo',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}
    attachment2 = {'fileUrl':"https://docs.google.com/spreadsheets/d/"+sheet.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.spreadsheet'}
    return [attachment1, attachment2]    

def copySuperCasual(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '1IOokmwp6Q4VRrgq0ZwsAIs1bTMlhu15CZ6Y8kMOa_qw',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()

    
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}
    
    return [attachment1]

def copySuperCorp(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '1AjHcUdcPE6Ky33-LIvqr8GB_7mZteHmbYn_pI11cvMU',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()

    
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}

    return [attachment1]

def copyMoriarty(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '1dG6xEYqX3J0OR1VIoKtmi23pqVgOjtD7CVDy9jHYOPo',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()

    sheet = drive_service.files().copy(body = file_metadata,
                                      fileId = '1M_-1_H4o8IshKVX-6prWCl6rSVAwcNVm8gf8QVcECBw',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}
    attachment2 = {'fileUrl':"https://docs.google.com/spreadsheets/d/"+sheet.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.spreadsheet'}
    return [attachment1, attachment2]

def copyMoriartyCorp(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '15NMMSZZXPdnNQpjyP-37Xvu2p_VOL0_Zfy0TTeEcdxE',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()

    sheet = drive_service.files().copy(body = file_metadata,
                                      fileId = '1M_-1_H4o8IshKVX-6prWCl6rSVAwcNVm8gf8QVcECBw',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}
    attachment2 = {'fileUrl':"https://docs.google.com/spreadsheets/d/"+sheet.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.spreadsheet'}
    return [attachment1, attachment2]

def copyReturnToTreasure(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '1jenpkmACwvxQVlNYCOqvWoNhXzBtSqwK7vlFVrzyfj0',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}
    t = [attachment1]
    return t

def copyMinutesToMidnight(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '1wI_It0vGnYUyZjfCdOU9lQnw0jV2JRUDFr6Nq9SIBKU',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                   'title':filename,
                   'mimeType':'application/vnd.google-apps.document'}
    t = [attachment1]
    return t

def copyRememberGhosts(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '1Ho8jg5uZqh8UR6y_jCUQ7MJkk_snBJLTLXnXbmNmse8',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}
    t = [attachment1]
    return t

def copyMagiciansMansion(filename):
    file_metadata = {'name': filename}
    file = drive_service.files().copy(body = file_metadata,
                                      fileId = '1Qs0Ugz7ZpM1QcIqHCyHoNtRqtrIO6VWPLIG5LeMI_Tc',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment1 = {'fileUrl':"https://docs.google.com/document/d/"+file.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}
    powerpoint = drive_service.files().copy(body = file_metadata,
                                      fileId = '1cgTV5XKi_guMXCRgkppAWhY04Y_JEfHUG34piaozsiw',
                                      ignoreDefaultVisibility = True,
                                      fields = 'id').execute()
    attachment2 = {'fileUrl':"https://docs.google.com/presentation/d/"+powerpoint.get('id'),
                    'title':filename,
                    'mimeType':'application/vnd.google-apps.document'}                
    t = [attachment1, attachment2]
    return t

def decider(roomName,date, time, counted, multi):
    
    if multi:
        filename = roomName + " "+str(date)+ " " + str(time)+ "-0"+ str(counted)
    else:
        filename = roomName + " "+str(date)+ " " + str(time)

    if roomName == "The Nancy Drew Virtual Escape Room":
        temp = copyNancyCasual(filename)
        return temp

    elif roomName == "Return to Treasure Island Virtual Escape Room":
        temp = copyReturnToTreasure(filename)
        return temp
    
    elif roomName == "Remember the Ghosts of Christmas - Virtual Escape Room":
        temp = copyRememberGhosts(filename)
        return temp

    elif roomName == "The Nancy Drew Virtual Team Building Escape Room - Coordination":
        temp = copyNancyCorp(filename)
        return temp

    elif roomName == "Moriarty's Parlor - Virtual Escape Room":
        temp = copyMoriarty(filename)
        return temp

    elif roomName ==  "Sherlock vs. Moriarty - Virtual Team Building - Learning Agility":
        temp = copyMoriartyCorp(filename)
        return temp

    elif roomName == "The Superhero Virtual Team Building Escape Room - Collaboration":
        temp = copySuperCorp(filename)
        return temp

    elif roomName == "The Superhero Virtual Escape Room":
        temp = copySuperCasual(filename)
        return temp

    elif roomName == "The Minutes to Midnight Virtual Team Building Escape Room":
        temp = copyMinutesToMidnight(filename)
        return temp
    elif roomName == "The Enchanted Forest - Virtual Escape Room":
        temp = [] #copyMinutesToMidnight(filename)
        return temp

    elif roomName == "Magicians Mansion Virtual Escape Room":
    	temp = copyMagiciansMansion(filename)
    	return temp

    else:
        print("shit!")
        raise 
    
    
#uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
#downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')
#createFolder('Google')

#searchFile(1,"name contains 'Nancy'")
# print(copyNancyCasual("nc Test"))
# print(copyNancyCorp("nb Test"))
# print(copySuperCasual("sc Test"))
# print(copySuperCorp('sb Test'))
# print(copyMoriarty('mp test'))
#(copyMinutesToMidnight('mtm test'))

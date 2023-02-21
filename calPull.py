from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    tomorrow = datetime.datetime.now() + datetime.timedelta(hours=48)
    tomorrow = tomorrow.isoformat() + 'Z'
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#    print('Getting the upcoming 200 events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,
                                        maxResults=1000, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    t = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        temps = event['creator']
        emains = temps['email']
        if emains == 'guides@mysteryescaperoom.com':
            #print(str(event))
            start = event['start'].get('dateTime', event['start'].get('date'))
            t.append([event['summary'],start,event.get('attendees',[]),event['id']])

    return t

def addEmployee(id, email):
    creds = None
    # The file token.pickle stores the user's access and refresh tok>
    # created automatically when the authorization flow completes fo>
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user lo>
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # First retrieve the event from the API.
    event = service.events().get(calendarId='primary', eventId=id).execute()
    #print(event['attendees'])


    event['attendees'].append({'email':email})
    updated_event = service.events().update(calendarId='primary', eventId=id, body=event, sendUpdates="all").execute()

    # Print the updated date.
    print (updated_event['updated'])


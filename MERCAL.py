from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import filesMaker
from uuid import uuid4
import requests
import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

positionIds = {"The Superhero Virtual Escape Room":5323040, 
        "Sherlock vs. Moriarty - Virtual Team Building - Learning Agility":5877475,
        "The Superhero Virtual Team Building Escape Room - Collaboration":5323043,
        "The Minutes to Midnight Virtual Team Building Escape Room":5323046,
        "Moriarty's Parlor - Virtual Escape Room":5416153,
        "Return to Treasure Island Virtual Escape Room":5742624,
        "Remember the Ghosts of Christmas - Virtual Escape Room":6004762,
        "The Nancy Drew Virtual Escape Room":5323045,
        "The Adventures of Sherlock Holmes, Moriarty's Parlor - Tucson, Arizona":2160356,
        "The Curse of Pharaoh's Tomb - Tucson, Arizona":2160356,
        "Dracula's Castle Haunted Escape - Tucson, Arizona":2160356,
        "The Sword of Zorro - Salt Lake City, Utah":5990827,
        "20,000 Leagues Under the Sea - Tucson, Arizona":2160356,
        "Sherlock Holmes and the Hound of the Baskervilles - St. George, Utah":4374064,
        "Christmas Toyland - St. George, Utah":6082782,
        "Christmas Toyland - Salt Lake City, Utah":6072675,
        "The Nancy Drew Virtual Team Building Escape Room - Coordination":5371793,
        "The Mirror Ghost's Haunted Basement - Salt Lake City, Utah":5990822,
        "Nancy Drew and Hardy Boys Hidden Chamber\" - St. George Utah\"":5954498,
        "Nancy Drew: The Mystery of the Missing Jewelry - Salt Lake City, Utah":5990823,
        "The Secrets of Downton Abbey - Salt Lake City, Utah":5990824,
        "The Ghost's of Christmas - Tucson":2160356,
        "The Enchanted Forest - Virtual Escape Room":6426945,
        "TUS - Houdini's Magic Escape Room":2160356,
        "Magicians Mansion Virtual Escape Room":6695930}

locationIds= {"The Superhero Virtual Escape Room":5323039,
	"Magicians Mansion Virtual Escape Room":5323039,
	"The Enchanted Forest - Virtual Escape Room":5323039, 
        "Sherlock vs. Moriarty - Virtual Team Building - Learning Agility":5323039,
        "The Superhero Virtual Team Building Escape Room - Collaboration":5323039,
        "The Minutes to Midnight Virtual Team Building Escape Room":5323039,
        "Moriarty's Parlor - Virtual Escape Room":5323039,
        "Return to Treasure Island Virtual Escape Room":5323039,
        "Remember the Ghosts of Christmas - Virtual Escape Room":5323039,
        "The Nancy Drew Virtual Escape Room":5323039,
        "The Adventures of Sherlock Holmes, Moriarty's Parlor - Tucson, Arizona":5537065,
        "The Curse of Pharaoh's Tomb - Tucson, Arizona":2160356,
        "Dracula's Castle Haunted Escape - Tucson, Arizona":5537065,
        "The Sword of Zorro - Salt Lake City, Utah":5571343,
        "20,000 Leagues Under the Sea - Tucson, Arizona":5537065,
        "Sherlock Holmes and the Hound of the Baskervilles - St. George, Utah":2160344,
        "Christmas Toyland - St. George, Utah":2160344,
        "Christmas Toyland - Salt Lake City, Utah":5571343,
        "The Nancy Drew Virtual Team Building Escape Room - Coordination":5323039,
        "The Mirror Ghost's Haunted Basement - Salt Lake City, Utah":5571343,
        "Nancy Drew and Hardy Boys Hidden Chamber\" - St. George Utah\"":2160344,
        "Nancy Drew: The Mystery of the Missing Jewelry - Salt Lake City, Utah":5571343,
        "The Secrets of Downton Abbey - Salt Lake City, Utah":5571343,
        "The Ghost's of Christmas - Tucson":5537065,
        "TUS - Houdini's Magic Escape Room":5537065}

slingUrl = "https://api.getsling.com/shifts/bulk"

slingToken = "b4ccbc98e0fe4934acbf9f5d72c6071f"



def main(memail, mroom, mdate, mtime, mquantity, phoneNumber, lastName, firstName ):
    
    mtime = mtime[0:6]
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
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    count = 0
    email = memail
    room = mroom
    date = mdate
    time = mtime
    quantity = mquantity
    quantity = int(quantity)
    startTime=date+'T'+time+":00"
    endTime=date+'T'+str(int(time[:2])+1)+str(time[2:])+":00"
    #event = room
    if quantity > 1:
        multi = True
        counted = 1
    else:
        multi = False
        counted = 1
    for i in range(quantity):
    #makes Google Documents    
        if multi:
            roomr = room + "-0"+str(counted)
            filelst = filesMaker.decider(room, date, time, counted, multi)
            
        else:
            roomr = room
            filelst =filesMaker.decider(room, date, time, counted, multi)
        creationTime = datetime.datetime.now(pytz.timezone('America/Denver'))
        if len(filelst) > 0:
            t = filelst[0]
        if len(filelst) > 2 :
            sevents = filelst[1]
            s = str(sevents["fileUrl"])
            
        else:
            s = ""
            event = {
            'summary': roomr,
            'description': 'Mystery Escape Room - Virtual Escape Room \n \nThanks for booking one of our online escape room adventures. Here is the information that you will need to know for the event to go well. The online adventure takes place in an online meeting format and there will be a website that will contain your mission. You and your team will be exploring and gathering clues from multiple places on the web, so the event is best done on a computer with web meeting capabilities. Tablets and phones do not give participants full access to all the event has to offer. If you would like to use a meeting system of your own, ie, Zoom, MS Teams, Webex, etc. please send an invite to david@mysteryescaperoom.com\nCustomer Name: '+firstName+' '+lastName+'\nCustomer Contact Email: '+email+'\nCustomer Contact Phone Number: '+str(phoneNumber)+'\n\nEvent made at: '+str(creationTime),
            'start': {
            'dateTime': startTime,
            'timeZone' : "America/Denver",
            },
            'end': {
            'dateTime': endTime,
            'timeZone' : "America/Denver",
            },
            'conferenceData' :  {"createRequest": {"requestId": f"{uuid4().hex}",
            "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
            'attachments':filelst,
            'attendees': [
            {'email':email}
            ],
            'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'popup', 'minutes': 30},
            ],
            },
            }
            #httplib2.debuglevel = 4
            event = service.events().insert(calendarId='primary', body=event, supportsAttachments=True, sendUpdates='all', conferenceDataVersion = 1).execute()
            print ('Event created: %s' % (event.get('id')))
            location = locationIds[room]
            position = positionIds[room]
            data ="[{\"available\":true,\"type\":\"shift\",\"slots\":1,\"dtstart\": \""+startTime+"\",\"dtend\": \""+endTime+"\",\"location\": { \"id\": "+str(location)+" },\"position\": { \"id\": "+str(position)+" },\"summary\":\""+email+"\"}]"
            headers = {
                'Content-Type': 'application/json',
                'Authorization':slingToken,
                'accept': '*/*',
            }
            if location != 5323039:
                quantity = 1
            #print(data)
            response = requests.request("POST",slingUrl, headers=headers, data=data)
            print(response)
            count +=1
            counted +=1
    print("Events Made: "+str(count))



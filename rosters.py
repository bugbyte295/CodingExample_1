# make positionsIds Dict edited each time a new position is made
import pytz
import json
import requests
import datetime
import time
import calPull
#make sure to not mess this up
positionIds = {"Superhero Casual":"The Superhero Virtual Escape Room",
"Sherlock vs Moriarty Corporate":"Sherlock vs. Moriarty - Virtual Team Building - Learning Agility",
"Superhero Corporate":"The Superhero Virtual Team Building Escape Room - Collaboration",
"Minutes to Midnight Corporate":"The Minutes to Midnight Virtual Team Building Escape Room",
"Moriarty's Parlor Casual":"Moriarty's Parlor - Virtual Escape Room",
"Pirates Casual":"Return to Treasure Island Virtual Escape Room",
"Ghost of Christmas Casual":"Remember the Ghosts of Christmas - Virtual Escape Room",
"Nancy Casual":"The Nancy Drew Virtual Escape Room",
"Nancy Corporate":"The Nancy Drew Virtual Team Building Escape Room - Coordination",
"The Enchanted Forest":"The Enchanted Forest - Virtual Escape Room",
"Magicians Mansion Casual":"Magicians Mansion Virtual Escape Room"}


def main():
	#get all shifts
	headers = {
	    'accept': 'application/json',
	    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
	}

	response = requests.get('https://api.sling.is/v1/groups', headers=headers)
	positionDict = {}
	positionLst = json.loads(response.text)
	#keep track of posisiton IDs w/ Names
	for i in range(len(positionLst)):
	    dict = positionLst[i]
	    positionDict[int(dict['id'])] = str(dict['name'])
	#Get all employees
	headers = {
	    'accept': 'application/json',
	    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
	}

	response = requests.get('https://api.sling.is/v1/users', headers=headers)
	userDict = {}
	userLst =  json.loads(response.text)
	empEmail = []
	#dictionary of employee ids and Email addresses
	for i in range(len(userLst)):
	    dict = userLst[i]
	    userDict[int(dict['id'])] = str(dict['email'])
	    empEmail.append(str(dict['email']))
	empEmail.remove('les@mysteryescaperoom.com')
	#get roster of the next day rooms
	headers = {
	    'accept': 'application/json',
	    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
	}

	today = datetime.datetime.now(pytz.timezone('America/Denver')).strftime('%Y-%m-%d')
	tomorrow = datetime.datetime.now() + datetime.timedelta(hours=40)
	tomorrow = tomorrow.strftime('%Y-%m-%d')
	params = (
	    ('dates', today+"/"+tomorrow),
	)

	response = requests.get('https://api.sling.is/v1/reports/roster', headers=headers, params=params)
	#print(str(response))
	respDict = json.loads(response.text)
	#print(str(respDict))
	#returns calendar events (set to 200) if over 200 rooms in the day need to change
	calEvents = calPull.main()

	shiftsList = []
	#shifts sorted and put into a list
	for i in range(len(respDict)):
	    t = respDict[i]
	    location = t['location']
	    if location['id'] == 5323039:
	        user = t['user']
	        users = userDict[int(user['id'])]
	        pos = t['position']
	        positions = positionDict[int(pos['id'])]
	        sum = t['summary']
	        start = t['dtstart']
	        shiftsList.append([start[11:16],str(positions),str(users),sum,pos['id']])
	# go through each event
	for i in range(len(calEvents)):
	    event = calEvents[i]
	    #print(str(event))
	    s = False
	    t = 0
	    temp = []
	    attendees = event[2]
	# make a list of attendees
	    for k in range(len(attendees)):
	        v = attendees[k]
	        emailed = v['email']
	        temp.append(str(emailed).lower())
	# go go go        
	    for i in range(len(temp)):
	        if temp[i] in empEmail:
	            s = True
#	            print("dup")
	    while not s:
	        shift = shiftsList[t]
	        positiond = (shift[1])
	        id = event[3]
	#        print(id)
	        try:
	            sdsd = positionIds[positiond]
	        except KeyError:
	            sdsd = "null"
	        # email in shift in the attendee list and the shift is in the event
	        tt = event[1]
	        if str(shift[3]).lower() in temp and sdsd in event[0] and str(shift[0]) == str(tt[11:16]):
	           # print(shift[2]+ " "+str(temp)+" "+event[0]+"\n")
#	            print(id + " " + shift[2])
	            calPull.addEmployee(id,shift[2])
#	            print(str(shift))
#	            print(str(event))
	            s = True 
	            #have to delete shift so there aren't duplicates
	            del shiftsList[t]
	        #wrong shift
	        else:
	            t +=1
	#no shifts match the event. Pass the event
	            if t > len(shiftsList) -1:
	                s = True
#	                print("Null: "+str(temp)+","+str(event[0]))

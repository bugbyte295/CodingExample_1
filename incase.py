# make positionsIds Dict edited each time a new position is made
import pytz
import json
import requests
import datetime
import time
import calPull

positionIds = {"Superhero Casual":"The Superhero Virtual Escape Room",
"Sherlock vs Moriarty Corporate":"Sherlock vs. Moriarty - Virtual Team Building - Learning Agility",
"Superhero Corporate":"The Superhero Virtual Team Building Escape Room - Collaboration",
"Minutes to Midnight Corporate":"The Minutes to Midnight Virtual Team Building Escape Room",
"Moriarty's Parlor Casual":"Moriarty's Parlor - Virtual Escape Room",
"Pirates Casual":"Return to Treasure Island Virtual Escape Room",
"Ghost of Christmas Casual":"Remember the Ghosts of Christmas - Virtual Escape Room",
"Nancy Casual":"The Nancy Drew Virtual Escape Room",
"Nancy Corporate":"The Nancy Drew Virtual Team Building Escape Room - Coordination"}


headers = {
    'accept': 'application/json',
    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
}

response = requests.get('https://api.sling.is/v1/groups', headers=headers)
positionDict = {}
#print (response.text)
positionLst = json.loads(response.text)
#print(positionLst)
for i in range(len(positionLst)):
    dict = positionLst[i]
    positionDict[int(dict['id'])] = str(dict['name'])

#print(str(positionDict))

headers = {
    'accept': 'application/json',
    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
}

response = requests.get('https://api.sling.is/v1/users', headers=headers)
userDict = {}
userLst =  json.loads(response.text)
for i in range(len(userLst)):
    dict = userLst[i]
    userDict[int(dict['id'])] = str(dict['name'] + ' '+dict['lastname'])


headers = {
    'accept': 'application/json',
    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
}
#today = time.strftime("%Y-%m-%d")
today = datetime.datetime.now(pytz.timezone('America/Denver')).strftime('%Y-%m-%d')
#print(today)
params = (
    ('dates', today),
)

response = requests.get('https://api.sling.is/v1/reports/roster', headers=headers, params=params)

#print(response)

#print(type(response.text))
respDict = json.loads(response.text)
#print(type(respDict))
#print("\n"*5)
#print(str(respDict))

calEvents = calPull.main()
#print(len(calEvents))
shiftsList = []
#shifts
for i in range(len(respDict)):
    t = respDict[i]
  #  print(t['summary'])
    location = t['location']
    if location['id'] == 5323039:
       # print(t['summary'])
      #  print(str(t) + "\n"*2)  
	#position
	#employee name/email
        user = t['user']
        users = userDict[int(user['id'])]
        pos = t['position']
        positions = positionDict[int(pos['id'])]
        sum = t['summary']
        start = t['dtstart']
        shiftsList.append([start[11:16],str(positions),str(users),sum,pos['id']])
#        input('next')

#print(str(shiftsList))
#input()

for i in range(len(calEvents)):
    event = calEvents[i]
    #print(event[0])
    s = False
    t = 0
#    print(event)
    temp = []
    attendees = event[2]
    #print(str(attendees)+"\n"*3)
    for k in range(len(attendees)):
        v = attendees[k]
        emailed = v['email']
        temp.append(str(emailed).lower())
    #print(str(temp))
    while not s:
        shift = shiftsList[t]
        #print(shift)
        positiond = (shift[1])
#        try:
#            sdsd = positionIds[positiond]
#        except KeyError:
#            break
#            s = True
#            print("fuck")
#        print("shift: "+sdsd)

#        print("event: "+event[0])
        #print("l: "+ shift[3])
        if str(shift[3]).lower() in temp:
            print(shift[2]+ " "+str(temp)+" "+event[0]+"\n")
            s = True
#            del calEvents[i]
            del shiftsList[t]
            #print("cool")
        else:
            t +=1    
            #print(t)
#check to make sure room is correct as well
            if t > len(shiftsList) -1:
                s = True
                print("Null")

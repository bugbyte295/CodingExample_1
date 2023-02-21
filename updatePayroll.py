import os
import json
import requests
import pprint
from datetime import date, timedelta
casual = [2160356,5323040,6049114,5323045,5416153,5878794,5742624,5942371,6004762,6426945,6695930]
corp = [5323043,5323046,5371793,5877475]
partial = [5688391]

headers = {
    'accept': 'application/json',
    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
}

response = requests.get('https://api.sling.is/v1/users/concise', headers=headers)

usersJSON = json.loads(response.text)
usersJSON = usersJSON['users']

userDict = {}

for user in usersJSON:
    if user["active"] == True and 5323040 in user['groupIds']:
        userDict[user['id']] = [user['name'], user['lastname'],0,0,0,0,0,0,user['groupIds']] #2corp, 3cas, 4part, 5early, 6extra early, 7total

#pprint.pprint(userDict)

def payrollSystem(s,e): #truples
    #YYYY - MM - DD
    sdatea = date(s)
    edatea = date(e)
    delta = edatea - sdatea
    for i in range(delta.days + 1):
        day = sdatea + timedelta(days=i)
        #print(str(day))
        headers = {
            'accept': 'application/json',
            'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
            }
        params = (
            ('dates', str(day)+"/"+str(day)),
            )
        response = requests.get('https://api.sling.is/v1/reports/roster', headers=headers, params=params)
        l = json.loads(response.text)
        #.pprint(sched)
        #input()
        #l = (json.dumps(t).replace("\\","")[2:-3]+ "\n") 
        #l = json.loads(sche[0]) #list

        for i in range(len(l)):
            #process each shift need dict of employees, positions, 
            shift = l[i] #dict
            loc = shift["location"]
            if loc["id"] == 5323039:
                try:
                    empl = userDict[shift["user"]["id"]]
                except KeyError:
                    continue
                try:
                    pos = shift["position"]["id"]
                except KeyError:
                    continue
                tim = int(shift["dtstart"][11:13])
                #print(tim)
                if tim <9 or tim > 21:
                    if tim < 7 or tim > 23:
                        empl[5] += 1
                        #print(tim)
                    elif tim < 9 or tim > 21: 
                        empl[6] += 1
                        #print(tim)
                if pos in corp:
                    empl[2] += 1
                    
                elif pos in casual:
                    empl[3] += 1
                elif pos in partial:
                    empl[4] += 1
                #print(str(empl))
                userDict[shift["user"]["id"]] = empl
    #pprint.pprint(userDict)
    
    # Trainee = 7848744
    # Guide = 7848749
    # Master guide = 7848750
    #values[8] = positions

    for k in userDict:
        values = userDict[k]
        #print(values[8])
        
        if 7848749 in values[8]:
            values[7] += values[2]*22 + values[3]*17 + values[4]*5 + values[5]*10 + values[6]*5
        elif 7848750 in values[8]:
            values[7] += values[2]*23 + values[3]*18 + values[4]*5 + values[5]*10 + values[6]*5
        elif 7848744 in values[8]:
            values[7] += values[2]*13 + values[3]*13 + values[4]*5 + values[5]*10 + values[6]*5
        else:
            pass
    for t in userDict:
        k = userDict[t]
        print(k[0]+" "+k[1]+" - "+str(k[7]))

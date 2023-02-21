import os
import json
from datetime import date, timedelta
casual = [2160356,5323040,6049114,5323045,5416153,5878794,5742624,5942371,6004762,6426945,6695930]
corp = [5323043,5323046,5371793,5877475]
partial = [5688391]

emplDict = {}
employees = open("employeeConfig.csv", "r")
for line in employees:
    line = line.strip()
    line = line.split(",")
    emplDict[int(line[0])] = [0,0,0,0,0,line[1], line[2], 0 ]

def main(sdate, edate): #truples
    sdatea = date(sdate[0],sdate[1],sdate[2])
    edatea = date(edate[0],edate[1],edate[2])
    delta = edatea - sdatea
    for i in range(delta.days + 1):
        day = sdatea + timedelta(days=i)
        #print(str(day))
        t = os.popen("bash roster b4ccbc98e0fe4934acbf9f5d72c6071f "+str(day)+"/"+str(day)).readlines()
        #l = (json.dumps(t).replace("\\","")[2:-3]+ "\n") 
        l = json.loads(t[0]) #list

        for i in range(len(l)):
            #process each shift need dict of employees, positions, 
            shift = l[i] #dict
            loc = shift["location"]
            if loc["id"] == 5323039:
                try:
                    empl = emplDict[shift["user"]["id"]]
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
                        empl[3] += 1
                        #print(tim)
                    elif tim < 9 or tim > 21: 
                        empl[4] += 1
                        #print(tim)
                if pos in corp:
                    empl[0] += 1
                    
                elif pos in casual:
                    empl[1] += 1
                elif pos in partial:
                    empl[2] += 1
                #print(str(empl))
                emplDict[shift["user"]["id"]] = empl
    #print(str(emplDict))
    for k in emplDict:
        values = emplDict[k]
        #print(values)
        if values[6] == "G":
            values[7] += values[0]*22 + values[1]*17 + values[2]*5 + values[3]*10 + values[4]*5
        elif values[6] == "MG":
            values[7] += values[0]*23 + values[1]*18 + values[2]*5 + values[3]*10 + values[4]*5
        elif values[6] == "T":
            values[7] += values[0]*13 + values[1]*13 + values[2]*5 + values[3]*10 + values[4]*5
        else:
            pass
        #print(values[5]+", "+str(values[7]))
    
main([2021,5,16],[2021,5,31])

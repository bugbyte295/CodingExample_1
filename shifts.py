import json
import requests

headers = {
    'accept': 'application/json',
    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
}

response = requests.get('https://api.sling.is/v1/groups', headers=headers)

#print (response.text)

respDict = json.loads(response.text)
#print(type(respDict))

for i in range(len(respDict)):
    #print(str(respDict[i]) + "\n"*2)

import requests
import json

headers = {
    'accept': 'application/json',
    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
}

response = requests.get('https://api.sling.is/v1/users', headers=headers)

print(response)
respDict = json.loads(response.text)
print(type(respDict))

for i in range(len(respDict)):
    t = respDict[i]
    print(str(t) + "\n"*2)

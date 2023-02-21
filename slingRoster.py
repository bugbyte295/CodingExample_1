import requests
import time
url = "https://api.getsling.com/reports/roster"

token = "b4ccbc98e0fe4934acbf9f5d72c6071f"

#data = "[{\"dates\":\"2020-12-29\"}]"

params = (('dates','2020-12-29'),)

headers = {'Content-Type': 'application/json',
    'Authorization': token,
    'accept': '*/*',
    }

response = requests.request("GET", url, headers=headers, params=params)

#print(response)

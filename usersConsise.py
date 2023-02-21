import requests
import pprint
fin = open("out.txt","w")

headers = {
    'accept': 'application/json',
    'Authorization': 'b4ccbc98e0fe4934acbf9f5d72c6071f',
}

response = requests.get('https://api.sling.is/v1/users/concise', headers=headers)

fin.write(pprint.pformat(response.text))
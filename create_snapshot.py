import json
import sys
import requests

authtoken=sys.argv[1]
mirrorsetselfurl=sys.argv[2]
Headers2 = {'Authorization':'Token '+ authtoken}
body = {}
mirrorset=[]
mirrorset.append(mirrorsetselfurl)
body['mirrorset']=mirrorset
print body
r = requests.post("https://aasemble.com/api/v1/snapshots/", data=body, headers=Headers2)
print r.content
values = json.loads(r.content)
print values["self"]


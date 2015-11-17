import json
import sys
import requests

authtoken=sys.argv[1]
mirrorselfurl=sys.argv[2]
Headers2 = {'Authorization':'Token '+ authtoken}
body = {}
mirrors=[]
mirrors.append(mirrorselfurl)
body['mirrors']=mirrors
#body=json.dumps(body)
print body
r = requests.post("https://aasemble.com/api/v1/mirror_sets/", data=body, headers=Headers2)
print r.content
values = json.loads(r.content)
print values["self"]


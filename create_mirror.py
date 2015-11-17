import json
import sys
import requests

authtoken=sys.argv[1]
mirrorurl=sys.argv[2]
mirrorseries=sys.argv[3]
mirrorcomponent=sys.argv[4]
Headers2 = {'Authorization':'Token '+ authtoken}
body = {}
body['url']=mirrorurl
series=[]
series.append(mirrorseries)
components=[]
components.append(mirrorcomponent)
body['series']=series
body['components']=components
body['public']=True
#body=json.dumps(body)
print body
r = requests.post("https://aasemble.com/api/v1/mirrors/", data=body, headers=Headers2)
print r.content
values = json.loads(r.content)
print values["self"]


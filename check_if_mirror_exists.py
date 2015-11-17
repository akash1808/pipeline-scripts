import json
import sys
import httplib
import requests

authtoken=sys.argv[1]
mirrorurl=sys.argv[2]
mirrorseries=sys.argv[3]
mirrorcomponent=sys.argv[4]
Headers2 = {'Authorization':'Token '+ authtoken}
print Headers2
r = requests.get("https://aasemble.com/api/v2/mirrors/", headers=Headers2)
print r.content
seriesbool=False
componentsbool=False
result=False
#data=sys.argv[1]
#print data
values = json.loads(r.content)
for count in range(0,values["count"]):

    print values["results"][count]
    mirrors = values["results"][count]
    print count
    print mirrors
    print mirrors['url']
    series = set(mirrors["series"])
    components = set (mirrors["components"])
    if ((mirrorseries in series) and (mirrorcomponent in components) and (mirrorurl == mirrors['url'])):
        result=True
        break

if result:
    print mirrors["self"]

else:
    os.system("python create_mirror.py authtoken mirrorurl mirrorseries mirrorcomponent")

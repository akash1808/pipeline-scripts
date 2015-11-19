import json
import sys
import httplib
import requests

authtoken=sys.argv[1]
mirrorselfurl=sys.argv[2]
print mirrorselfurl
Headers2 = {'Authorization':'Token '+ authtoken}
print Headers2
r = requests.get("https://aasemble.com/api/v2/mirror_sets/", headers=Headers2)
print r.content
seriesbool=False
componentsbool=False
result=False
#data=sys.argv[1]
#print data
values = json.loads(r.content)
for count in range(0,values["count"]):

    print values["results"][count]
    mirrorsets = values["results"][count]
    print count
    print mirrorsets
    print mirrorsets['mirrors']
    mirrorset = mirrorsets["mirrors"]
    print mirrorset
    print mirrorselfurl    
    if ((len(mirrorset) == len(mirrorselfurl)) and
   (all(i in mirrorset for i in mirrorselfurl))):
        print 'True'
    else:
        print 'False'
    print set(mirrorselfurl) == set(mirrorset)
    if (set(mirrorselfurl) == set(mirrorset)):
        result=True
        break

if result:
    print mirrorsets["self"]

#else:
#    os.system("python create_mirror.py authtoken mirrorurl mirrorseries mirrorcomponent")

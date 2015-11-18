import json
import sys
import requests
import time

authtoken=sys.argv[1]
mirrorselfurl=sys.argv[2]
Headers2 = {'Authorization':'Token '+ authtoken}
url = mirrorselfurl+"refresh/"
body={}
print url
r = requests.post(url, headers=Headers2)
print r.content
refresh_happened=False
while(not refresh_happened):
    time.sleep(2)
    r = requests.get(mirrorselfurl, data=body, headers=Headers2)
    print r.content
    values=json.loads(r.content)
    refresh_happenning=values["refresh_in_progress"]
    print "refresh_in_progress:"
    print refresh_happenning 
    refresh_happened= not refresh_happenning
    time.sleep(5)

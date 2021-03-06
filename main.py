import json
import sys
import httplib
import requests
import time

authtoken=sys.argv[1]
mirrorurl=sys.argv[2]
mirrorseries=sys.argv[3]
mirrorcomponent=sys.argv[4]


def create_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent):
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
    r = requests.post("http://54.254.240.24/api/v2/mirrors/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return values["self"]


def check_for_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent):
    Headers2 = {'Authorization':'Token '+ authtoken}
    r = requests.get("http://54.254.240.24/api/v2/mirrors/", headers=Headers2)
    seriesbool=False
    componentsbool=False
    result=False
    values = json.loads(r.content)
    if (values["count"] > 0):
        for count in range(0,values["count"]):
            mirrors = values["results"][count]
            series = set(mirrors["series"])
            components = set (mirrors["components"])
            if ((mirrorseries in series) and (mirrorcomponent in components) and (mirrorurl == mirrors['url'])):
                result=True
                break

        if result:
            trigger_mirror_update(authtoken, mirrors["self"])
            return mirrors["self"]

        else:
            return create_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent)
    else:
         return create_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent)
def trigger_mirror_update(authtoken,mirrorurl):
    Headers2 = {'Authorization':'Token '+ authtoken}
    url = mirrorurl+"refresh/"
    body={}
    r = requests.post(url, headers=Headers2)
    refresh_happened=False
    while(not refresh_happened):
        time.sleep(2)
        r = requests.get(mirrorurl, data=body, headers=Headers2)
        values=json.loads(r.content)
        refresh_happenning=values["refresh_in_progress"]
        refresh_happened= not refresh_happenning
        time.sleep(5)

def create_mirror_set(authtoken,mirrorselfurl):
    Headers2 = {'Authorization':'Token '+ authtoken}
    body = {}
    mirrors=[]
    mirrors.append(mirrorselfurl)
    body['mirrors']=mirrors
    r = requests.post("http://54.254.240.24/api/v2/mirror_sets/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return values["self"]


def check_for_mirror_set(authtoken,mirrorselfurl):
    Headers2 = {'Authorization':'Token '+ authtoken}
    r = requests.get("http://54.254.240.24/api/v2/mirror_sets/", headers=Headers2)
    seriesbool=False
    componentsbool=False
    result=False
    values = json.loads(r.content)
    for count in range(0,values["count"]):
        mirrorsets = values["results"][count]
        mirrorset = set(mirrorsets["mirrors"])
        if ((mirrorselfurl in mirrorset)):
            result=True
            break

    if result:
        return mirrorsets["self"]

    else:
        return create_mirror_set(authtoken,mirrorselfurl)


def create_snapshot(authtoken,mirrorsetselfurl):
    Headers2 = {'Authorization':'Token '+ authtoken}
    body = {}
    mirrorset=[]
    mirrorset.append(mirrorsetselfurl)
    body['mirrorset']=mirrorset
    r = requests.post("http://54.254.240.24/api/v2/snapshots/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return values["self"]    


def main(authtoken,mirrorurl,mirrorseries,mirrorcomponent):
    mirrorselfurl=check_for_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent)
    mirrorsetselfurl=check_for_mirror_set(authtoken,mirrorselfurl)
    snapshot=create_snapshot(authtoken,mirrorsetselfurl)
    return snapshot


if __name__ == "__main__":
     print(main(authtoken,mirrorurl,mirrorseries,mirrorcomponent))

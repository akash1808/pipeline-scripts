import json
import sys
import httplib
import requests
import yaml

def read_from_yaml(authtoken,filename):
    with open(filename, 'r') as f:
        doc = yaml.load(f)
        count=len(doc['repositories'])
        mirrors=[]
        for x in doc['repositories']:
            mirror=check_for_mirror( authtoken,x["location"],x["release"],x["repos"])
            mirrors.append(mirror)
    return mirrors

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
    r = requests.post("https://aasemble.com/api/v2/mirrors/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return values["self"]


def check_for_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent):
    Headers2 = {'Authorization':'Token '+ authtoken}
    r = requests.get("https://aasemble.com/api/v2/mirrors/", headers=Headers2)
    seriesbool=False
    componentsbool=False
    result=False
    values = json.loads(r.content)
    for count in range(0,values["count"]):
        mirrors = values["results"][count]
        series = set(mirrors["series"])
        components = set (mirrors["components"])
        if ((mirrorseries in series) and (mirrorcomponent in components) and (mirrorurl == mirrors['url'])):
            result=True
            break

    if result:
        return mirrors["self"]

    else:
        return create_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent)


def create_mirror_set(authtoken,mirrorselfurl):
    Headers2 = {'Authorization':'Token '+ authtoken}
    body = {}
    body['mirrors']=mirrorselfurl
    r = requests.post("https://aasemble.com/api/v2/mirror_sets/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return values["self"]


def check_for_mirror_set(authtoken,mirrorselfurl):
    Headers2 = {'Authorization':'Token '+ authtoken}
    r = requests.get("https://aasemble.com/api/v2/mirror_sets/", headers=Headers2)
    seriesbool=False
    componentsbool=False
    result=False
    values = json.loads(r.content)
    for count in range(0,values["count"]):
        mirrorsets = values["results"][count]
        mirrorset = set(mirrorsets["mirrors"])
        mirrorselfurl1 = set(mirrorselfurl)
        if ((mirrorselfurl1 == mirrorset)):
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
    r = requests.post("https://aasemble.com/api/v2/snapshots/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return values["self"]    


def main(authtoken,filename):
    mirrorselfurl=read_from_yaml(authtoken,filename)
    mirrorsetselfurl=check_for_mirror_set(authtoken,mirrorselfurl)
    snapshot=create_snapshot(authtoken,mirrorsetselfurl)
    return snapshot


if __name__ == "__main__":
     sys.exit(main(authtoken,filename))

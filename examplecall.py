import yaml
import json
import multiple_repos
import sys

authtoken=sys.argv[1]
filename=sys.argv[2]
snapshot=multiple_repos.main(authtoken,filename)
print snapshot

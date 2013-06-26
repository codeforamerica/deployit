import json
from deploy_config import load_config

def last_deploy(*deploy_names):

    last_deploys = {}
    deploy_names = list(deploy_names)

    for line in reversed(open("deployments.log.json", "r").readlines()):

        deploy = json.loads(line)
        if(deploy['name'] in deploy_names):
            last_deploys[deploy['name']]  = deploy
            deploy_names.remove(deploy['name'])

    return last_deploys


def deployment(deployment=None):

    hist = load_config('deployments.log.json')
    hist['deploys'].append(json.dumps({"name":deployment['name'], 
            "timestamp": deployment['time'], 
            "sha": deployment['sha']}))

    f = open('deployments.log.json', 'w')
    f.write(json.dumps(hist))


def deploy_details(deployment, line):

    #log stdin/stderr to tmp dir, for debugging deploys.

    pass


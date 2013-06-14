import json

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

    with open("deployments.log.json", "a") as f:
        f.write(json.dumps({"name":"deploy a", "timestamp": 1234}) + "\n")


def deploy_details(deployment, line):

    #log stdin/stderr to tmp dir, for debugging deploys.

    pass

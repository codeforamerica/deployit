import subprocess
import os
import time
from git import *
from deploy_history import deploy_details, deployment



def run_deploy(config, target_name):
    # Based on the config of the project, choose type of deploy

    target = get_target(config, target_name)

    if("gitDestRemote" in target):
        run_git_deploy(config, target)
    else:
        run_generic_deploy(config, target)

def get_target(config, target):

    for t in config['targets']:
        if(t['name'] == target):
            return t

    return None

def run_git_deploy(config, target):
    # git pull, git push
    # capture stdout/stderr
    # http://stackoverflow.com/questions/1606795/catching-stdout-in-realtime-from-subprocess

    #pull or clone it
    run_cmd(["git", "clone", config['gitSourceRemote'], config['key']], path="./repos")
    run_cmd(["git", "pull", config['gitSourceRemote'], "master"], path="./repos/"+config["key"])
    #push it (right now just back where it came from)
    run_cmd(["git", "push", "origin", "master"], path="./repos/"+config["key"])

    #TODO: Get timestamp from run_cmd output?
    repo = Repo("./repos/"+config['key'])
    headcommit = repo.commit('master')
    config['sha'] = headcommit.hexsha
    config['time'] = time.time()
    deployment(config)



def run_generic_deploy(config):
    #git pull, then run other commands define in config to build and deploy.
    pass





def run_cmd(cmd, path=None):

    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         cwd=path)

    for line in iter(p.stdout.readline, b''):
        print(">>> " + line.rstrip())

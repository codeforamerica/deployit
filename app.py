import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import flash
from git_auth import *
from deploy_config import load_config
from deploy import run_deploy
import json


app = Flask(__name__)
#Move to env
app.debug = True

app.secret_key = os.environ['DEPLOYIT_KEY_SECRET']
config = load_config("config.json")

gh = Github(app)


@app.route("/login")
def login():
    return gh.git_authorize(url_for('oauthorized', _external=True))


@app.route('/oauthorized')
@gh.gh.authorized_handler
def oauthorized(resp):

    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash('Github Authorization Failed') 
        return redirect(url_for('index'))

    github_token = resp['access_token']
    session['github_token'] = resp['access_token'], ''

    if gh.user_in_team(config['auth_org'], config['dep_team']):
            session['deployer'] = True
            return redirect(url_for('index'))
    else:
        flash("You do not have deployment permissions.")
        return redirect(url_for('index'))


@app.route("/")
def index():
    return render_template('index.html', deployables=config['deployables'])

@app.route("/logout")
def logout():
    session.pop('github_token', None)
    session.pop('deployer', None)
    return redirect(url_for('index'))

@app.route("/currentCommits", methods=['GET'])
def github_commits():
    gh_commits = gh.get_repo_commits(config['auth_org'], repo)
    if not gh_commits:
        return json.dumps(None)

    deploys = load_config('deployments.log.json')['deploys']
    last_dep = deploys[len(deploys) - 1]

    for i in range(len(gh_commits)):
        if commits[i]['sha'] == last_dep['sha']:
            commits = commits[:i]
            break

    return json.dumps(commits)


@app.route("/deploy", methods=['POST'])
def deploy():
    #Run the deploy, and stream the stderr/stout

    deployable = config['deployables'][request.form['deployable']]
    deployable['key'] = request.form['deployable']

    run_deploy(deployable, request.form['target'])


    return "DONE"


@gh.gh.tokengetter
def get_github_token(token=None):
    return session.get('github_token')


if __name__ == "__main__":
    app.run()

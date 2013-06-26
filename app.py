import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import flash
from flask_oauthlib.client import OAuth
from deploy_config import load_config
from deploy import run_deploy
import json


app = Flask(__name__)
#Move to env
app.debug = True

app.secret_key = os.environ['DEPLOYIT_KEY_SECRET']
GH_CLIENT_ID = os.environ['DEPLOYIT_GH_ID']
GH_CLIENT_SECRET = os.environ['DEPLOYIT_GH_SECRET']

config = load_config("config.json")

oauth = OAuth(app)
github = oauth.remote_app('github',
	consumer_key=GH_CLIENT_ID,
	consumer_secret=GH_CLIENT_SECRET,
	request_token_params={'scope': 'user,public_repo'},
	base_url='https://api.github.com/',
	request_token_url=None, 
	access_token_method='POST',
	access_token_url='https://github.com/login/oauth/access_token',
	authorize_url='https://github.com/login/oauth/authorize'
)


@app.route("/login")
def login():
	return github.authorize(callback=url_for('oauthorized', _external=True))


@app.route('/oauthorized')
@github.authorized_handler
def oauthorized(resp):
	next_url = request.args.get('next') or url_for('index')
	if resp is None:
		flash('Github Authorization Failed')
		return redirect(url_for('index'))

	github_token = resp['access_token']
	session['github_token'] = github_token, ''

	user = github.get('/user').data
	orgs = github.get('/user/orgs')

	cfa_id = None
	team_id = None
	for org in orgs.data:
		if org['login'] == config['auth_org']:
			cfa_id = org['id']
			break

	if not cfa_id:
		flash("You must be a %s Org member." % config['auth_org'])
		return redirect(url_for('index'))

	teams = github.get('/orgs/%s/teams' % config['auth_org'])
	if teams.status != 200:
		flash("Could not fetch your org's teams.")
	for team in teams.data:
		if team['name'] == config['dep_team']:
			team_id = team['id']
			break

	deployers = github.get('/teams/%s/members' % team_id)
	if deployers.status != 200:
		flash("Could not find the configured deployment team")
		return redirect(url_for('index'))

	for deployer in deployers.data:
		if deployer['id'] == user['id']:
			#TODO: Move deployer out of session into g
			session['deployer'] = True
			return redirect(url_for('index'))

	if not session['deployer']:
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
    # fetch most recent commit for a project on github.
	# change this to correct repo
	gh_commits = github.get('repos/%s/%s/commits' % (config['auth_org'],
		request.form['deployable']))

	commits = []
	for commit in gh_commits.data:
		commits.append({'author': commit['commit']['author']['name'],
			'message': commit['commit']['message'], 'sha': commit['sha'],
			'date': commit['commit']['author']['date']})

	deploys = load_config('deployments.log.json')

	last_dep = deploys['deploys'][len(deploys) - 1]

	for i in range(len(commits)):
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


@github.tokengetter
def get_github_token(token=None):
	return session.get('github_token')

if __name__ == "__main__":
    app.run()

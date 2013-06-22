import os
from flask_oauthlib.client import OAuth
from flask import flash


GH_CLIENT_ID = os.environ['DEPLOYIT_GH_ID']
GH_CLIENT_SECRET = os.environ['DEPLOYIT_GH_SECRET']
class Github:
    def __init__(self, app):
        self.app = app
        self.oauth = OAuth(app)
        self.gh = self.oauth.remote_app('github',
            consumer_key=GH_CLIENT_ID,
            consumer_secret=GH_CLIENT_SECRET,
            request_token_params={'scope': 'user,public_repo'},
            base_url='https://api.github.com/',
            request_token_url=None, 
            access_token_method='POST',
            access_token_url='https://github.com/login/oauth/access_token',
            authorize_url='https://github.com/login/oauth/authorize'
        )

    def git_authorize(self, callback_url):
        return self.gh.authorize(callback=callback_url)

    def checked_get_req(self, url, info_type):
        request = self.gh.get(url)
        if request.status != 200:
            flash("Could not fetch %s information.")
            return False
        return request.data

    def user_in_org(self, org):

        org_id = None
        orgs = self.checked_get_req('/user/orgs', 'organizations')
        if (orgs):
            for anorg in orgs:
                if anorg['login'] == org:
                    org_id = anorg['id']
                    return True

        if not org_id:
            return False

    def user_in_team(self, org, team):

        if not self.user_in_org(org):
            flash("You must be a %s Org member." % config['auth_org'])
            return False

        team_id = None
        teams = self.checked_get_req('/orgs/%s/teams' % org, 'teams')
        user = self.checked_get_req('/user', 'user')
        if teams and user:
            for ateam in teams:
                if ateam['name'] == team:
                    team_id = ateam['id']
                    break
        else:
            return False

        if not team_id:
            flash("No such team in this Org, check your configuration")
            return False


        deployers = self.checked_get_req('/teams/%s/members' % team_id, 'deployment team')
        if deployers:
            for deployer in deployers:
                if deployer['id'] == user['id']:
                    return True

        return False

    def get_repo_commits(self, owner, repo):
        gh_commits = github.checked_get_req(github, 'repos/%s/%s/commits' % (owner, repo))
        # Pulls necessary data out of the query, need more info? Add it here.
        commits = []
        for commit in gh_commits:
            commits.append({'author': commit['commit']['author']['name'],
                'message': commit['commit']['message'], 'sha': commit['sha'],
                'date': commit['commit']['author']['date']})
        return commits



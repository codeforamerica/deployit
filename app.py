from flask import Flask
from flask import render_template
from flask import request
from deploy_config import load_config
from deploy import run_deploy

app = Flask(__name__)

# Move to env
app.debug = True


config = load_config("config.json")


@app.route("/")
def index():

    return render_template('index.html', deployables=config['deployables'])



@app.route("/currentCommits")
def github_commits():

    # fetch most recent commit for a project on github.
    return ""



@app.route("/deploy", methods=['POST'])
def deploy():

    #Run the deploy, and stream the stderr/stout

    deployable = config['deployables'][request.form['deployable']]
    deployable['key'] = request.form['deployable']

    run_deploy(deployable, request.form['target'])




    return "DONE"


if __name__ == "__main__":
    app.run()

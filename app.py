from flask import Flask
from flask import render_template
from deploy_config import load_config


app = Flask(__name__)
app.debug = True


config = load_config("config.json")


@app.route("/")
def index():

    return render_template('index.html', deployables=config['deployables'])

@app.route("/currentCommits")
def github_commits:

    # fetch most recent commit for each proejct to see if there are things to deploy.
    return ""



@app.route("/deploy")
def deploy:

    # stream the logs?

    return "DONE"


if __name__ == "__main__":
    app.run()

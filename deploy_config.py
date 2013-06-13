import json



def load_config(filename):

    f = open(filename, "r")
    config = json.loads(f.read())
    return config

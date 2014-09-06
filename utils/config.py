import json
import os

def get_paths():
    paths = json.loads(open(os.path.join(os.path.dirname(__file__), "SETTINGS.json")).read())
    for key in paths:
        paths[key] = os.path.expandvars(paths[key])
    return paths

def get_path(path, file_name):
    return os.path.join(get_paths()[path], file_name)

def get_config():
    config = json.loads(open(get_paths()["config"]).read())
    return config

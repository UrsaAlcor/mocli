import os
import json

from appdirs import user_config_dir
from simplejson import load


NAME = 'mocli'
AUTHOR = 'mocli'
CONFIG = user_config_dir(NAME, AUTHOR)
CONFIGNAME = 'loc.json'
LATEST_CONF = None


def load_conf():
    global LATEST_CONF
    config = os.path.join(CONFIG, CONFIGNAME)
    os.makedirs(CONFIG, exist_ok=True)

    try:
        with open(config, 'r') as conffile:
            conf = json.load(conffile)
    except FileNotFoundError:
            conf = dict()

    LATEST_CONF = conf
    return conf


def save_conf(conf):
    config = os.path.join(CONFIG, CONFIGNAME)
    os.makedirs(CONFIG, exist_ok=True)

    with open(config, 'w') as conffile:
        json.dump(conf, conffile)


def update_conf(**kwargs):
    conf = load_conf()
    conf.update(kwargs)
    save_conf(conf)


def option(name, default=None):
    return load_conf().get(name, default)

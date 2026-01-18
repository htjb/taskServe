"""Main entry point for taskserve."""

from .app import app
import os
import yaml

def main():
    try:
        with open(os.path.expanduser('~') + '/.config/taskServe.yml', 'r') as stream:
            config = yaml.safe_load(stream)
        hostIP = config['host_IP']
    except (FileNotFoundError, KeyError) as e:
        print("TASKSERVE: No host_IP specified in '~/.config/taskServe.yml'. Defaulting to '0.0.0.0'.")
        config={}
        condig['hostIP']='0.0.0.0'

    app.run(host=config['host_IP'], port=5678)

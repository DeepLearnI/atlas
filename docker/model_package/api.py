import click

def break_click_echo(*args, **kwargs):
    pass

click.echo = break_click_echo
click.secho = break_click_echo

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
import logging

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

def job_root():
    from os import environ

    job_id = environ['JOB_ID']
    return '/archive/archive/{}/artifacts'.format(job_id)

def job_manifest():
    import yaml

    with open(f'{job_root()}/foundations_package_manifest.yaml', 'r') as manifest_file:
        return yaml.load(manifest_file.read())

def module_name_and_function_name():
    manifest = job_manifest()
    prediction_definition = manifest['entrypoints']['predict']

    return prediction_definition['module'], prediction_definition['function']

def move_to_job_directory():
    import sys
    import os

    root_of_the_job = job_root()
    sys.path.insert(0, root_of_the_job)
    os.chdir(root_of_the_job)

def add_module_to_sys_path(module_name):
    import sys
    import os.path

    module_path = module_name.replace('.', '/')
    module_directory = os.path.dirname(module_path)
    if module_directory:
        module_directory = f"{job_root()}/{module_directory}"
        sys.path.insert(0, module_directory)

def load_prediction_function():
    import importlib

    move_to_job_directory()
    module_name, function_name = module_name_and_function_name()
    add_module_to_sys_path(module_name)

    module = importlib.import_module(module_name)
    return getattr(module, function_name)

prediction_function = load_prediction_function()

class ServeModel(Resource):
    def get(self):
        return {'message': 'still alive'}

    def post(self):
        data = dict(request.json)
        return prediction_function(**data)

api.add_resource(ServeModel, '/')

if __name__ == '__main__':
    app.logger.disabled = True
    app.run(debug=False, port=80, host='0.0.0.0')
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from tabulate import tabulate

class CommandLineInterface(object):

    def __init__(self, args):
        from foundations_contrib.cli.sub_parsers.setup_parser import SetupParser
        from foundations_contrib.cli.sub_parsers.orbit_parser import OrbitParser

        self._input_arguments = args

        self._argument_parser = self._initialize_argument_parser()
        self._subparsers = self._argument_parser.add_subparsers()

        SetupParser(self).add_sub_parser()
        OrbitParser(self).add_sub_parser()

        self._initialize_init_parser()
        self._initialize_submit_parser()
        self._initialize_info_parser()
        self._initialize_retrieve_parser()
        self._initialize_stop()
        self._initialize_clear_queue()
        self._initialize_delete_parser()

    def add_sub_parser(self, name, help=None):
        sub_parser = self._subparsers.add_parser(name, help=help)
        sub_parser.add_argument('--debug', action='store_true', help='Sets debug mode for the CLI')
        return sub_parser

    def _initialize_stop(self):
        stop_parser = self.add_sub_parser('stop', help='Stops a running job')
        stop_parser.add_argument('scheduler_config', metavar='scheduler-config', help='Environment the job is running in')
        stop_parser.add_argument('job_id', type=str, help='Specify job ID of running job')
        stop_parser.set_defaults(function=self._stop)

    def _initialize_clear_queue(self):
        clear_queue_parser = self.add_sub_parser('clear-queue', help='Clears all scheduled jobs from the queue')
        clear_queue_parser.add_argument('scheduler_config', metavar='scheduler-config', help='Environment to clear the queue')
        clear_queue_parser.set_defaults(function=self._clear_queue)

    def _initialize_delete_parser(self):
        delete_parser = self.add_sub_parser('delete', help='Delete items from execution environment')
        delete_subparsers = delete_parser.add_subparsers()
        self._initialize_delete_job_parser(delete_subparsers)

    def _initialize_delete_job_parser(self, delete_subparsers):
        delete_job_parser = delete_subparsers.add_parser('job', help='Delete jobs')
        delete_job_parser.add_argument('scheduler_config', type=str, help='Environment to delete job from')
        delete_job_parser.add_argument('job_id', type=str, help='Specify job ID of already deployed job')
        delete_job_parser.set_defaults(function=self._delete_job)

    def _initialize_argument_parser(self):
        from argparse import ArgumentParser
        argument_parser = ArgumentParser(prog='foundations')
        argument_parser.add_argument('--version', action='store_true', help='Displays the current Foundations version')
        argument_parser.add_argument('--debug', action='store_true', help='Sets debug mode for the CLI')
        argument_parser.set_defaults(function=self._no_command)
        return argument_parser

    def _initialize_init_parser(self):
        init_parser = self.add_sub_parser('init', help='Creates a new Foundations project in the current directory')
        init_parser.add_argument('project_name', type=str, help='Name of the project to create')
        init_parser.set_defaults(function=self._init)

    def _initialize_submit_parser(self):
        from argparse import REMAINDER
        deploy_parser = self.add_sub_parser('submit', help='Deploys a Foundations project to the specified environment')
        deploy_parser.add_argument('--entrypoint', type=str, help='Command process will execute with (default: python)')
        deploy_parser.add_argument('--project-name', help='Project name for job (default: base name of cwd directory)')
        deploy_parser.add_argument('--num-gpus', type=int, help='A non-zero value will run a GPU-enabled job with all available GPUs. Does not currently support allocate GPU quantity (default: 0)')
        deploy_parser.add_argument('--ram', type=float, help='GB of RAM to allocate for job (default: no limit)')
        deploy_parser.add_argument('--stream-job-logs', type=self._str_to_bool, default=True, help='Whether or not to stream job logs (default: True)')
        deploy_parser.add_argument('scheduler_config', metavar="scheduler-config", help='Environment to run file in')
        deploy_parser.add_argument('job_directory', type=str, metavar="job-directory", help='Directory from which to deploy')
        deploy_parser.add_argument('command', type=str, nargs=REMAINDER, help='Arguments to be used by the entrypoint')
        deploy_parser.set_defaults(function=self._submit)
        deploy_parser.set_defaults(params={})

    @staticmethod
    def _str_to_bool(string_value):
        return string_value == 'True'

    def _initialize_info_parser(self):
        info_parser = self.add_sub_parser('info', help='Provides information about your Foundations project')
        info_parser.add_argument('--env', action='store_true')
        info_parser.set_defaults(function=self._info)

    def _initialize_model_serve_parser(self):
        serving_parser = self.add_sub_parser('serve', help='Used to serve models in Atlas')
        serving_subparsers = serving_parser.add_subparsers()

        serving_deploy_parser = serving_subparsers.add_parser('start')
        serving_deploy_parser.add_argument('--project_name', required=True, type=str, help='The user specified name for the project that the model will be added to')
        serving_deploy_parser.add_argument('job_id')
        serving_deploy_parser.set_defaults(function=self._kubernetes_model_serving_deploy)

        serving_destroy_parser = serving_subparsers.add_parser('stop')
        serving_destroy_parser.add_argument('--project_name', required=True, type=str, help='The user specified name for the project that the model will be added to')
        serving_destroy_parser.add_argument('model_name')
        serving_destroy_parser.set_defaults(function=self._kubernetes_model_serving_destroy)

    def _initialize_retrieve_parser(self):
        retrieve_parser = self.add_sub_parser('get', help='Get file types from execution environments')
        retrieve_subparsers = retrieve_parser.add_subparsers()
        self._initialize_retrieve_artifact_parser(retrieve_subparsers)
        self._initialize_retrieve_logs_parser(retrieve_subparsers)

    def _initialize_retrieve_artifact_parser(self, retrieve_subparsers):
        retrieve_artifact_parser = retrieve_subparsers.add_parser('job', help='Specify job to retrieve artifacts from')
        retrieve_artifact_parser.add_argument('scheduler_config', type=str, help='Environment to get from')
        retrieve_artifact_parser.add_argument('job_id', type=str, help="Specify job uuid of already deployed job")
        retrieve_artifact_parser.add_argument('--save_dir', type=str, default=None, help="Specify local directory path for artifacts to save to. Defaults to directory within current working directory")
        retrieve_artifact_parser.add_argument('--source_dir', type=str, default='', help="Specify relative directory path to download artifacts from. Default will download all artifacts from job")
        retrieve_artifact_parser.set_defaults(function=self._retrieve_artifacts)

    def _initialize_retrieve_logs_parser(self, retrieve_subparsers):
        retrieve_logs_parser = retrieve_subparsers.add_parser('logs', help='Get logs for jobs')
        retrieve_logs_parser.add_argument('scheduler_config', type=str, help='Environment to get from')
        retrieve_logs_parser.add_argument('job_id', type=str, help='Specify job uuid of already deployed job')
        retrieve_logs_parser.set_defaults(function=self._retrieve_logs)

    def _initialize_serving_stop_parser(self, serving_subparsers):
        serving_deploy_parser = serving_subparsers.add_parser('stop', help='Stop foundations model package server')
        serving_deploy_parser.set_defaults(function=self._model_serving_stop)

    def execute(self):
        from foundations_contrib.global_state import log_manager

        self._arguments = self._argument_parser.parse_args(self._input_arguments)
        try:
            self._arguments.function()
        except Exception as error:
            if self._arguments.debug == True:
                raise
            else:
                print(f'Error running command: {error}')
                exit(1)

    def arguments(self):
        return self._arguments

    def arguments(self):
        return self._arguments

    def _no_command(self):
        import foundations

        if self._arguments.version:
            print('Running Foundations version {}'.format(foundations.__version__))
        else:
            self._argument_parser.print_help()

    def _init(self):
        from foundations_contrib.cli.scaffold import Scaffold

        project_name = self._arguments.project_name
        result = Scaffold(project_name).scaffold_project()
        if result:
            print('Success: New Foundations project `{}` created!'.format(project_name))
        else:
            print('Error: project directory for `{}` already exists'.format(project_name))

    def _info(self):
        from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher

        env_name = self._arguments.env

        if not env_name:
            print('usage: foundations info [--env ENV]')
            return

        project_environment, global_environment = EnvironmentFetcher().get_all_environments()

        if len(global_environment) == 0 and (project_environment == None or len(project_environment) == 0):
            print('No environments available')
        else:
            self._print_configs('submission', global_environment)
            if project_environment != None:
                self._print_configs('execution', project_environment)

    def _print_configs(self, config_list_name, config_list):
        config_list = self._create_environment_list(config_list)
        print("\n{} configs:".format(config_list_name))
        if len(config_list) == 0:
            print('No {} environments available'.format(config_list_name))
        else:
            print(self._format_environment_printout(config_list))

    def _format_environment_printout(self, environment_array):
        return tabulate(environment_array, headers = ['env_name', 'env_path'])

    def _create_environment_list(self, available_environments):
        import os
        environment_names = []
        for env in available_environments:
            environment_names.append([env.split(os.path.sep)[-1].split('.')[0], env])
        return environment_names
   
    def _submit(self):
        from foundations_contrib.cli.job_submission.submit_job import submit
        submit(self._arguments)

    def _retrieve_artifacts(self):
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.archiving.artifact_downloader import ArtifactDownloader
        from foundations_contrib.archiving import get_pipeline_archiver_for_job
        from foundations_contrib.cli.job_submission.config import load
        from foundations_contrib.change_directory import ChangeDirectory
        import os

        env_name = self._arguments.scheduler_config
        job_id = self._arguments.job_id
        current_directory = os.getcwd()

        if self._arguments.save_dir is None:
            self._arguments.save_dir = os.path.join(current_directory, str(job_id))

        with ChangeDirectory(current_directory):
            load(self._arguments.scheduler_config or 'scheduler')

        job_deployment_class = config_manager['deployment_implementation']['deployment_type']
        job_deployment = job_deployment_class(job_id, None, None)

        job_status = job_deployment.get_job_status()

        if job_status is None:
            self._fail_with_message('Error: Job `{}` does not exist for environment `{}`'.format(job_id, env_name))
        else:
            if job_deployment.get_job_archive():
                print(f"Successfully retrieved Job {job_id} from archive store")
            else:
                print(f"Error: Could not download Job {job_id}")


    def _retrieve_logs(self):
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.cli.job_submission.config import load
        from foundations_contrib.change_directory import ChangeDirectory
        import os

        env_name = self._arguments.scheduler_config
        job_id = self._arguments.job_id
        current_directory = os.getcwd()

        with ChangeDirectory(current_directory):
            load(self._arguments.scheduler_config or 'scheduler')

        job_deployment_class = config_manager['deployment_implementation']['deployment_type']
        job_deployment = job_deployment_class(job_id, None, None)

        job_status = job_deployment.get_job_status()

        if job_status is None:
            self._fail_with_message('Error: Job `{}` does not exist for environment `{}`'.format(job_id, env_name))
        elif job_status == 'queued':
            self._fail_with_message('Error: Job `{}` is queued and has not produced any logs'.format(job_id))
        else:
            logs = job_deployment.get_job_logs()
            print(logs)

    def _delete_job(self):
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.cli.job_submission.config import load
        from foundations_contrib.change_directory import ChangeDirectory
        import os

        env_name = self._arguments.scheduler_config
        job_id = self._arguments.job_id
        current_directory = os.getcwd()

        with ChangeDirectory(current_directory):
            load(self._arguments.scheduler_config or 'scheduler')

        job_deployment_class = config_manager['deployment_implementation']['deployment_type']
        job_deployment = job_deployment_class(job_id, None, None)

        job_status = job_deployment.get_job_status()

        if job_status is None:
            self._fail_with_message('Error: Job `{}` does not exist for environment `{}`'.format(job_id, env_name))
        elif job_status in ('queued', 'running', 'pending'):
            self._fail_with_message('Error: Job `{}` has status `{}` and cannot be deleted'.format(job_id, job_status))
        else:
            if job_deployment.cancel_jobs([job_id])[job_id]:
                print(f"Job {job_id} successfully deleted")
            else:
                print(f"Could not completely delete job {job_id}. Please make sure that the job bundle exists under ~/.foundations/job_data/")

    def _load_configuration(self):
        from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
        from foundations_contrib.global_state import config_manager

        env_name = self._arguments.env
        env_file_path = EnvironmentFetcher().find_environment(env_name)

        if env_file_path and env_file_path[0]:
            config_manager.add_simple_config_path(env_file_path[0])
        else:
            self._fail_with_message('Error: Could not find environment `{}`'.format(env_name))

    def _fail_with_message(self, message):
        import sys

        print(message)
        sys.exit(1)

    def _deploy_model_package(self):
        import requests
        import sys

        response = requests.post('http://{}/v1/{}/'.format(self._arguments.domain, self._arguments.slug), json = {'model_id': self._arguments.model_id})
        if response.status_code == 201:
            print('Model package was deployed successfully to model server.')
        else:
            print('Failed to deploy model package to model server.', file=sys.stderr)
            sys.exit(11)

    def _kubernetes_model_serving_deploy(self):
        from foundations_contrib.cli.model_package_server import deploy
        from foundations_contrib.global_state import message_router

        message_router.push_message('model_served', {'job_id': self._arguments.job_id, 'project_name': self._arguments.project_name})
        deploy(self._arguments.project_name, self._arguments.job_id)

    def _kubernetes_model_serving_destroy(self):
        from foundations_contrib.cli.model_package_server import destroy
        destroy(self._arguments.project_name, self._arguments.model_name)

    def _stop(self):
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.cli.job_submission.config import load
        from foundations_contrib.change_directory import ChangeDirectory
        import os

        env_name = self._arguments.scheduler_config
        job_id = self._arguments.job_id
        current_directory = os.getcwd()

        with ChangeDirectory(current_directory):
            load(self._arguments.scheduler_config or 'scheduler')

        job_deployment_class = config_manager['deployment_implementation']['deployment_type']
        job_deployment = job_deployment_class(job_id, None, None)

        try:
            job_status = job_deployment.get_job_status()

            if job_status is None:
                self._fail_with_message('Error: Job `{}` does not exist for environment `{}`'.format(job_id, env_name))
            elif job_status == 'queued':
                self._fail_with_message('Error: Job `{}` is queued and cannot be stopped'.format(job_id))
            elif job_status == 'completed':
                self._fail_with_message('Error: Job `{}` is completed and cannot be stopped'.format(job_id))
            else:
                if job_deployment.stop_running_job():
                    print('Stopped running job {}'.format(job_id))
                else:
                    print('Error stopping job {}'.format(job_id))
        except AttributeError:
            print('The specified scheduler does not support this functionality')

    def _clear_queue(self):
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.cli.job_submission.config import load
        from foundations_contrib.change_directory import ChangeDirectory
        import os

        env_name = self._arguments.scheduler_config
        current_directory = os.getcwd()

        with ChangeDirectory(current_directory):
            load(self._arguments.scheduler_config or 'scheduler')

        job_deployment_class = config_manager['deployment_implementation']['deployment_type']

        try:
            num_jobs_dequeued = job_deployment_class.clear_queue()
            print('Removed {} job(s) from queue'.format(num_jobs_dequeued))
        except AttributeError:
            print('The specified scheduler does not support this functionality')
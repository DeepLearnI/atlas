"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from scheduler_acceptance.mixins.node_aware_mixin import NodeAwareMixin
import foundations
from foundations_contrib.global_state import config_manager

class TestGetJobLogs(Spec, NodeAwareMixin):

    @let
    def config_path(self):
        import os.path as path
        from foundations_contrib.utils import foundations_home

        return path.join(foundations_home(), 'config', 'local_scheduler.config.yaml')

    @let
    def fake_job_id(self):
        return self.faker.uuid4()

    @set_up_class
    def set_up_class(klass):
        klass.set_up_api()

    @set_up
    def set_up(self):
        config_manager.push_config()
        self._create_config()

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import current_foundations_context

        foundations.set_job_resources(num_gpus=0)
        self._delete_config()
        config_manager.pop_config()

    def test_get_logs_for_job_that_does_not_exist_prints_error_message(self):
        import subprocess

        error_message = 'Error: Job `{}` does not exist for environment `local_scheduler`'.format(self.fake_job_id)
        command_to_run = self._command_to_run_job(self.fake_job_id)
        cli_result = subprocess.run(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cli_stdout = cli_result.stdout
        cli_stdout = cli_stdout.decode().rstrip('\n').split('\n')[-1]

        self.assertEqual(1, cli_result.returncode)
        self.assertIn(error_message, cli_stdout)

    def test_get_logs_for_queued_job_prints_error_message(self):
        import subprocess
        from scheduler_acceptance.fixtures.stages import get_ram_in_gb_when_limit_set, get_ram_in_gb_when_limit_not_set

        largest_memory = self._get_memory_capacity_for_largest_node()
        foundations.set_job_resources(0, largest_memory * 0.51)

        get_ram_in_gb = foundations.create_stage(get_ram_in_gb_when_limit_set)
        get_ram_in_gb_when_limit_not_set = foundations.create_stage(get_ram_in_gb_when_limit_not_set)
        stage_get_ram_in_gb = get_ram_in_gb()
        stage_get_ram_in_gb_when_limit_not_set = get_ram_in_gb_when_limit_not_set()

        job = stage_get_ram_in_gb.run()
        self._wait_for_job_to_run(job)

        queued_job = stage_get_ram_in_gb_when_limit_not_set.run()
        queued_job_id = queued_job.job_name()

        error_message = 'Error: Job `{}` is queued and has not produced any logs'.format(queued_job_id)
        command_to_run = self._command_to_run_job(queued_job_id)
        cli_result = subprocess.run(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cli_stdout = cli_result.stdout
        cli_stdout = cli_stdout.decode().rstrip('\n').split('\n')[-1]

        self.assertEqual(1, cli_result.returncode)
        self.assertIn(error_message, cli_stdout)

    def test_get_logs_for_completed_job(self):
        import subprocess

        job = foundations.submit(job_dir='scheduler_acceptance/fixtures/job_logs', num_gpus=0)
        job.wait_for_deployment_to_complete()
        completed_job_id = job.job_name()
        self.assertEqual('completed', job.get_job_status())

        command_to_run = self._command_to_run_job(completed_job_id)
        cli_result = subprocess.run(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cli_stdout = cli_result.stdout
        cli_stdout = cli_stdout.decode().rstrip('\n')

        self.assertEqual(0, cli_result.returncode)
        self.assertIn('the quick brown fox jumps over the lazy dog', cli_stdout)

    def test_get_logs_for_running_job(self):
        import subprocess
        from time import sleep

        job = foundations.submit(job_dir='scheduler_acceptance/fixtures/job_logs', entrypoint='main_with_wait.py', num_gpus=0)
        self._wait_for_job_to_run(job)
        running_job_id = job.job_name()
        sleep(60)
        self.assertEqual('running', job.get_job_status())

        command_to_run = self._command_to_run_job(running_job_id)
        cli_result = subprocess.run(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cli_stdout = cli_result.stdout
        cli_stdout = cli_stdout.decode().rstrip('\n')

        self.assertEqual(0, cli_result.returncode)
        self.assertIn('the quick brown fox jumps over the lazy dog', cli_stdout)

    def _command_to_run_job(self, job_id):
        return ['python', '-m' 'foundations', 'get', 'logs', '--job_id', job_id, '--env', 'local_scheduler']

    @staticmethod
    def _wait_for_job_to_run(job):
        import time

        while job.get_job_status() == 'queued':
            time.sleep(0.5)

    def _create_config(self):
        from foundations import config_manager
        import yaml

        config_dictionary = {
            'results_config': {
                'archive_end_point': '/archive', 
                'redis_end_point': config_manager['redis_url']
            },
            'ssh_config': {
                'code_path': '/jobs',
                'host': config_manager['remote_host'],
                'key_path': '~/.ssh/id_foundations_scheduler',
                'port': 31222,
                'result_path': '/jobs',
                'user': 'job-uploader'
            },
            'cache_config': {'end_point': '/cache'},
            'job_deployment_env': 'scheduler_plugin',
            'obfuscate_foundations': False
        }

        with open(self.config_path, 'w') as config_file:
            yaml.dump(config_dictionary, config_file)

    def _delete_config(self):
        import os
        os.remove(self.config_path)


    

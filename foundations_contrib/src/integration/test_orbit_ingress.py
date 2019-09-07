"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Katherine Bancroft <k.bancroft@dessa.com>, 06 2018
"""

import subprocess
from typing import List
import os
import time

from foundations_spec import *
from foundations_contrib.cli import model_package_server
import foundations_contrib
class TestOrbitIngress(Spec):
    
    namespace = 'foundations-scheduler-test'

    @let
    def sleep_time(self):
        return 60

    @set_up_class
    def set_up(self):
        _run_command(['./integration/resources/fixtures/test_server/spin_up.sh'])

    @let
    def model_name(self):
        return 'model'

    @let
    def second_model_name(self):
        return 'modeltwo'

    @let
    def project_name(self):
        return 'project'
    
    @tear_down_class
    def tear_down(self):
        command = f'bash ./remove_deployment.sh project model'
        _run_command(command.split(), foundations_contrib.root() / 'resources/model_serving/orbit')
        try:
            command = f'bash ./remove_deployment.sh project modeltwo'
            _run_command(command.split(), foundations_contrib.root() / 'resources/model_serving/orbit')
        except:
            print('Second test may not have created the pod')

        _run_command(['./integration/resources/fixtures/test_server/tear_down.sh'])

    def test_first_served_model_can_be_reached_through_ingress_using_default_and_model_endpoint(self):
        _run_command(f'./integration/resources/fixtures/test_server/setup_test_server.sh {self.namespace} {self.project_name} {self.model_name}'.split())

        self._assert_endpoint_accessable('/projects/project/model/', 'Test Passed')
        self._assert_endpoint_accessable('/projects/project/model/predict', 'get on predict')
        self._assert_endpoint_accessable('/projects/project/model/evaluate', 'get on evaluate')

        self._assert_endpoint_accessable('/projects/project/', 'Test Passed')
        self._assert_endpoint_accessable('/projects/project/predict', 'get on predict')
        self._assert_endpoint_accessable('/projects/project/evaluate', 'get on evaluate')

    @skip('not yet ready ... working local but failing on jenkins')
    def test_second_served_model_can_be_accessed(self):
        _run_command(f'./integration/resources/fixtures/test_server/setup_test_server.sh {self.namespace} {self.project_name} {self.second_model_name}'.split())

        self._assert_endpoint_accessable('/projects/project/modeltwo/predict', 'get on predict')

    def _assert_endpoint_accessable(self, endpoint, expected_text):
        scheduler_host = os.environ.get('FOUNDATIONS_SCHEDULER_HOST', 'localhost')
        
        for _ in range(self.sleep_time):
            try:
                result = _run_command(f'curl http://{scheduler_host}:31998{endpoint} --connect-timeout 1'.split()).stdout.decode()
            except Exception as e:
                result = 'Failed to connect'
        self.assertEqual(expected_text, result)

def _run_command(command: List[str], cwd: str=None) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=True, cwd=cwd)
    except subprocess.TimeoutExpired as error:
        raise Exception(error.stderr.decode())
    except subprocess.CalledProcessError as error:
        raise Exception(error.stderr.decode())
    return result

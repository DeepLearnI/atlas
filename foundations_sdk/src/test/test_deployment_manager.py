"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch


class TestDeploymentManager(unittest.TestCase):

    class MockDeployment(object):

        def __init__(self, job_name, job, job_source_bundle):
            self._job_name = job_name

        def config(self):
            return {}

        def deploy(self):
            pass

        def job_name(self):
            return self._job_name

    class MockListing(object):

        def __init__(self):
            self.value = None

        def track_pipeline(self, name):
            self.value = name

    def setUp(self):
        from foundations.config_manager import ConfigManager
        from foundations.deployment_manager import DeploymentManager
        from foundations.pipeline import Pipeline
        from foundations.pipeline_context import PipelineContext
        from foundations.foundations_context import FoundationsContext

        self._listing = self.MockListing()

        self._config = ConfigManager()
        self._config['deployment_implementation'] = {
            'deployment_type': self.MockDeployment
        }

        self._config['project_listing_implementation'] = {
            'project_listing_type': self._mock_listing,
        }

        self._deployment_manager = DeploymentManager(self._config)

        self._pipeline_context = PipelineContext()
        self._pipeline = Pipeline(self._pipeline_context)
        self._foundations_context = FoundationsContext(self._pipeline)
        self._stage = self._pipeline.stage(self._method)

    def test_deploy_persisted_project_name(self):
        self._foundations_context.set_project_name('my project')
        self._deployment_manager.simple_deploy(self._stage, '', {})

        self.assertEqual('my project', self._listing.value)

    def test_deploy_persisted_project_name_different_name(self):
        self._foundations_context.set_project_name('project potato launcher')
        self._deployment_manager.simple_deploy(self._stage, '', {})

        self.assertEqual('project potato launcher', self._listing.value)

    @patch('foundations.null_pipeline_archive_listing.NullPipelineArchiveListing')
    def test_deploy_persisted_project_name_supports_default_listing(self, mock):
        mock.side_effect = self._mock_listing

        del self._config.config()['project_listing_implementation']

        self._foundations_context.set_project_name('my project')
        self._deployment_manager.simple_deploy(self._stage, '', {})

        self.assertEqual('my project', self._listing.value)

    @patch('logging.Logger.info')
    def test_deployment_manager_deploy_info_log(self, mock):
        deployment = self._deployment_manager.simple_deploy(
            self._stage, '', {})
        mock.assert_called_with(
            "Job '{}' deployed.".format(deployment.job_name()))

    def _mock_listing(self):
        return self._listing

    def _method(self):
        pass

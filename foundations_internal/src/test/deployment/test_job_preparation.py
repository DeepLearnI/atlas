"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_internal.deployment.job_preparation import prepare_job


class TestJobPreparation(Spec):

    queue_job_instance = let_mock()

    @let_now
    def queue_job(self):
        queue_job = self.patch('foundations_events.producers.jobs.QueueJob', ConditionalReturn())
        queue_job.return_when(self.queue_job_instance, self.message_router, self.pipeline_context)
        return queue_job

    message_router = let_mock()

    @let
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        return self.patch('foundations_contrib.global_state.config_manager', ConfigManager())

    @let
    def pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        return PipelineContext()

    @set_up
    def set_up(self):
        self._job = Mock()
        self._job.pipeline_context.return_value = self.pipeline_context
        self._run_data = {'some random data': self._random_uuid()}
        self._job.kwargs = self._run_data
        self._job_id = self._random_uuid()

        self.config_manager['deployment_implementation'] = 'some kind of deployment'

    def test_prepare_sets_job_id(self):
        prepare_job(self.message_router, self._job, self._job_id)
        self.assertEqual(self._job_id, self.pipeline_context.file_name)

    def test_prepare_sets_run_data(self):
        prepare_job(self.message_router, self._job, self._job_id)
        self.assertEqual(self._job.kwargs,
                         self.pipeline_context.provenance.job_run_data)

    def test_pushes_queue_message(self):
        prepare_job(self.message_router, self._job, self._job_id)
        self.queue_job_instance.push_message.assert_called_once()

    def test_raise_exception_when_no_deployment_set(self):
        del self.config_manager.config()['deployment_implementation']
        with self.assertRaises(ValueError) as error_context:
            prepare_job(self.message_router, self._job, self._job_id)
        
        self.assertIn('No environment found, please set deployment environments with foundations.set_environment', error_context.exception.args)

    def _random_uuid(self):
        from uuid import uuid4
        return str(uuid4())

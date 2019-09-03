"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations_spec.extensions import run_process


class TestJobDataProducers(unittest.TestCase):

    def setUp(self):
        from acceptance.cleanup import cleanup
        from foundations.global_state import redis_connection

        cleanup()
        self._redis = redis_connection
        self._redis.delete('foundations_testing_job_id')

    def test_produces_proper_data(self):
        from foundations_contrib.job_data_redis import JobDataRedis

        run_process(['python', 'success.py'], 'acceptance/fixtures/job_data_production', {'FOUNDATIONS_JOB_ID': 'successful_job'})
        all_job_data = JobDataRedis.get_all_jobs_data('job_data_production', self._redis, True)

        job_data = all_job_data[0]
        self.assertEqual('job_data_production', job_data['project_name'])
        self.assertEqual('successful_job', job_data['job_id'])
        self.assertEqual('trial', job_data['user'])
        self.assertEqual('completed', job_data['status'])
        self.assertTrue(isinstance(job_data['start_time'], float))
        self.assertTrue(isinstance(job_data['completed_time'], float))
        self.assertGreater(len(job_data['output_metrics']), 0)

    def test_produces_completed_job_data(self):
        from foundations_internal.fast_serializer import deserialize
        from time import time

        run_process(['python', 'success.py'], 'acceptance/fixtures/job_data_production', {'FOUNDATIONS_JOB_ID': 'successful_job'})
        current_time = time()

        serialized_metrics = self._redis.lrange(
            'jobs:successful_job:metrics', 0, -1)
        metrics = [deserialize(data) for data in serialized_metrics]
        metric_1, metric_2, metric_3 = metrics

        self.assertTrue(current_time - metric_1[0] < 2)
        self.assertTrue(current_time - metric_2[0] < 2)
        self.assertTrue(current_time - metric_3[0] < 2)

        self.assertEqual('hello', metric_1[1])
        self.assertEqual('hello', metric_2[1])
        self.assertEqual('world', metric_3[1])

        self.assertEqual(1, metric_1[2])
        self.assertEqual(2, metric_2[2])
        self.assertEqual(3, metric_3[2])

        metric_keys = self._redis.smembers(
            'project:job_data_production:metrics')
        metric_keys = set([data.decode() for data in metric_keys])
        self.assertEqual(set(['hello', 'world']), metric_keys)

        state = self._redis.get('jobs:successful_job:state').decode()
        self.assertEqual('completed', state)

        project_name = self._redis.get('jobs:successful_job:project').decode()
        self.assertEqual('job_data_production', project_name)

        user_name = self._redis.get('jobs:successful_job:user').decode()
        self.assertEqual('trial', user_name)

        completed_time = self._redis.get(
            'jobs:successful_job:completed_time').decode()
        completed_time = float(completed_time)
        self.assertTrue(current_time - completed_time < 2)

        start_time = self._redis.get('jobs:successful_job:start_time').decode()
        start_time = float(start_time)
        self.assertTrue(current_time - start_time > 0.01)
        self.assertTrue(current_time - start_time < 10)

        creation_time = self._redis.get(
            'jobs:successful_job:creation_time').decode()
        creation_time = float(creation_time)
        self.assertTrue(current_time - creation_time > 0.01)
        self.assertTrue(current_time - creation_time < 120)

        running_jobs = self._redis.smembers(
            'project:job_data_production:jobs:running')
        running_jobs = set([data.decode() for data in running_jobs])
        self.assertEqual(set(['successful_job']), running_jobs)
        
    def test_produces_failed_job_data(self):
        run_process(['python', 'fail.py'], 'acceptance/fixtures/job_data_production', {'FOUNDATIONS_JOB_ID': 'failed_job'})

        state = self._redis.get('jobs:failed_job:state').decode()
        self.assertEqual('failed', state)

        serialized_error_information = self._redis.get(
            'jobs:failed_job:error_information')
        error_information = self._foundations_deserialize(serialized_error_information)

        self.assertEqual("<class 'Exception'>", error_information['type'])

        self.assertEqual('', error_information['exception'])
        self.assertIsNotNone(error_information['traceback'])

    def _foundations_deserialize(self, serialized_value):
        from foundations_internal.foundations_serializer import deserialize
        return deserialize(serialized_value)
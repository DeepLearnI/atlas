
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from foundations_spec import *

@skip('skipped for now')
class TestJobsListingUIFriendly(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []
    tags = {'this_tag': 'this_value', 'that_tag': 'that_value'}

    @classmethod
    def setUpClass(klass):
        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name('lou')
        klass._make_completed_job_with_metrics('my job 3', 'bach', arg1='life', arg2=42, kwarg1='pi', kwarg2=3.14, tags=klass.tags)

    @classmethod
    def tearDownClass(klass):
        from foundations_contrib.global_state import redis_connection as redis
        redis.flushall()

    @classmethod
    def _prepare_job_input_data(klass, **kwargs):
        from foundations import Hyperparameter
        from foundations.stage_logging import log_metric

        def callback(arg1, arg2, kwarg1=None, kwarg2=None):
            log_metric('hello', 20)
            return ', '.join([str(arg1), str(arg2), str(kwarg1), str(kwarg2)])
        klass._pipeline.stage(
            callback, 
            Hyperparameter('arg1'), 
            Hyperparameter('arg2'), 
            kwarg1=Hyperparameter(), 
            kwarg2=Hyperparameter()
        ).run_same_process(**kwargs)

    @classmethod
    def _make_completed_job_with_metrics(klass, job_name, user, **kwargs):
        klass._pipeline_context.file_name = job_name
        klass._prepare_job_input_data(**kwargs)
        klass._make_completed_job(job_name, user, **kwargs)

    def test_get_route(self):
        data = super(TestJobsListingUIFriendly, self).test_get_route()
        job_data = data['jobs'][0]
        self.assertEqual(len(job_data['input_params']), 4)
        for obj in job_data['input_params']:
            self.assertEqual(len(obj), 4)
        for index, var_name in enumerate(['arg1', 'arg2', 'kwarg1', 'kwarg2']):
            self.assertEqual(job_data['input_params'][index]['name'], var_name)
        for index, var_type in enumerate(['string', 'number', 'string', 'number']):
            self.assertEqual(job_data['input_params'][index]['type'], var_type)
        for index, var_value in enumerate(['life', 42, 'pi', 3.14]):
            self.assertEqual(job_data['input_params'][index]['value'], var_value)
        for index in range(4):
            self.assertEqual(job_data['input_params'][index]['source'], 'placeholder')
        input_parameter_names = data['input_parameter_names']
        expected_input_parameter_names = [{'name': 'kwarg2', 'type': 'number'},
                                          {'name': 'kwarg1', 'type': 'string'},
                                          {'name': 'arg2', 'type': 'number'},
                                          {'name': 'arg1', 'type': 'string'}]
        self.assertCountEqual(input_parameter_names, expected_input_parameter_names)
        self.assertEqual(job_data['output_metrics'][0]['name'], 'hello')
        self.assertEqual(job_data['output_metrics'][0]['value'], 20)
        self.assertEqual(job_data['output_metrics'][0]['type'], 'number')
        self.assertEqual(self.tags, job_data['tags'])
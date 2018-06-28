"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from vcat.deployment_wrapper import DeploymentWrapper
import fixtures.deployment_wrapper_fixtures as dwf

class TestDeploymentWrapper(unittest.TestCase):
    def test_get_job_name(self):
        job_name = "job_name"

        deployment = DeploymentWrapper(dwf.MockDeployment(job_name))
        self.assertEqual(job_name, deployment.job_name())

    def test_get_different_job_name(self):
        job_name = "diff_name"

        deployment = DeploymentWrapper(dwf.MockDeployment(job_name))
        self.assertEqual(job_name, deployment.job_name())

    def test_is_job_complete_instantly_complete(self):
        deployment = DeploymentWrapper(dwf.InstantFinishDeployment("job_name"))
        self.assertTrue(deployment.is_job_complete())

    def test_is_job_complete_never_finish(self):
        deployment = DeploymentWrapper(dwf.NeverFinishDeployment("job_name"))
        self.assertFalse(deployment.is_job_complete())

    def test_is_job_complete_takes_one_second(self):
        deployment = DeploymentWrapper(dwf.TakesOneSecond("job_name"))

        for _ in range(0, 1):
            self.assertFalse(deployment.is_job_complete())

        self.assertTrue(deployment.is_job_complete())
        self.assertTrue(deployment.is_job_complete())

    def test_is_job_complete_takes_two_seconds(self):
        deployment = DeploymentWrapper(dwf.TakesTwoSeconds("job_name"))

        for _ in range(0, 2):
            self.assertFalse(deployment.is_job_complete())

        self.assertTrue(deployment.is_job_complete())
        self.assertTrue(deployment.is_job_complete())

    def test_wait_for_deployment_to_complete(self):
        deployment = DeploymentWrapper(dwf.SuccessfulTakesRandomTime("job_name"))

        self.assertIsNone(deployment._deployment.fetch_job_results())

        deployment.wait_for_deployment_to_complete(wait_seconds=0.1)
        
        result = deployment._deployment.fetch_job_results()
        self.assertIsNone(result["global_stage_context"]["error_information"])
        self.assertEqual(result["dummy_result"], "dummy_result")

    def test_fetch_job_results_failed_job(self):
        from vcat.remote_exception import RemoteException
        from vcat.utils import pretty_error
        import sys
        
        deployment = DeploymentWrapper(dwf.FailedMockDeployment("job_name"))

        try:
            result = deployment.fetch_job_results(wait_seconds=0.1)
            self.fail("RemoteException not thrown")
        except RemoteException as e:
            inner_result = deployment._deployment.fetch_job_results()
            self.assertEqual(str(e), pretty_error("job_name", inner_result["global_stage_context"]["error_information"]))

    def test_fetch_job_results_successful_job(self):
        deployment = DeploymentWrapper(dwf.SuccessfulMockDeployment("job_name"))

        result = deployment.fetch_job_results(wait_seconds=0.1)
        self.assertIsNone(result["global_stage_context"]["error_information"])
        self.assertEqual(result["dummy_result"], "dummy_result")

    def test_fetch_job_results_successful_takes_time(self):
        deployment = DeploymentWrapper(dwf.SuccessfulTakesTime("job_name"))

        result = deployment.fetch_job_results(wait_seconds=0.1)
        self.assertIsNone(result["global_stage_context"]["error_information"])
        self.assertEqual(result["dummy_result"], "dummy_result")

    def test_fetch_job_results_successful_takes_random_time(self):
        deployment = DeploymentWrapper(dwf.SuccessfulTakesRandomTime("job_name"))

        result = deployment.fetch_job_results(wait_seconds=0.1)
        self.assertIsNone(result["global_stage_context"]["error_information"])
        self.assertEqual(result["dummy_result"], "dummy_result")

    def test_fetch_job_results_failed_takes_random_time(self):
        from vcat.remote_exception import RemoteException
        from vcat.utils import pretty_error
        import sys
        
        deployment = DeploymentWrapper(dwf.FailedTakesRandomTime("job_name"))

        try:
            result = deployment.fetch_job_results(wait_seconds=0.1)
            self.fail("RemoteException not thrown")
        except RemoteException as e:
            inner_result = deployment._deployment.fetch_job_results()
            self.assertEqual(str(e), pretty_error("job_name", inner_result["global_stage_context"]["error_information"]))
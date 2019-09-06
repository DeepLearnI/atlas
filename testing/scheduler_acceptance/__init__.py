"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import scheduler_acceptance.config.remote_config
from scheduler_acceptance.test_can_run_job import TestCanRunJob
from scheduler_acceptance.test_cli_deployment import TestCliDeployment
from scheduler_acceptance.test_set_job_resources import TestSetJobResources
from scheduler_acceptance.test_get_job_logs import TestGetJobLogs
from scheduler_acceptance.test_obfuscate_jobs import TestObfuscateJobs
from scheduler_acceptance.test_cancel_queued_jobs import TestCancelQueuedJobs
from scheduler_acceptance.test_user_defined_scheduler_image import TestUserDefinedSchedulerImage
from scheduler_acceptance.test_tensorboard_endpoints import TestTensorboardEndpoint
from scheduler_acceptance.test_job_uses_venv_created_by_foundations import TestJobUsesVenvCreatedByFoundations

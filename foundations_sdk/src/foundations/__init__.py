"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def _check_if_in_cli():
    import traceback
    import os
    import os.path

    in_run_py = False
    in_unit_test = False
    for line in traceback.format_stack():
        if 'runpy.py' in line:
            in_run_py = True
        elif 'unittest' in line:
            in_unit_test = True

    if in_run_py and not in_unit_test:
        os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

_check_if_in_cli()

from foundations.hyperparameter import Hyperparameter
from foundations.job import Job
from foundations_internal.pipeline_archiver import PipelineArchiver
from foundations.context_aware import context_aware
from foundations.pipeline_archiver_fetch import PipelineArchiverFetch
from foundations.global_state import *
from foundations.deployment_utils import *
from foundations.job_persister import JobPersister
from foundations_contrib.null_archive import NullArchive
from foundations_contrib.null_pipeline_archive_listing import NullArchiveListing
from foundations_contrib.local_file_system_pipeline_archive import LocalFileSystemPipelineArchive
from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket
from foundations_contrib.local_file_system_pipeline_listing import LocalFileSystemPipelineListing
from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend
from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive
from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing
from foundations_contrib.prefixed_bucket import PrefixedBucket
from foundations_internal.serializer import *
from foundations_contrib.middleware.basic_stage_middleware import BasicStageMiddleware
from foundations_contrib.change_directory import ChangeDirectory
from foundations_contrib.bucket_job_deployment import BucketJobDeployment
from foundations_contrib.archiving.save_artifact import save_artifact
from foundations_contrib.deployment_wrapper import DeploymentWrapper
from foundations.projects import set_project_name, set_tag, get_metrics_for_all_jobs
from foundations_internal.scheduler import Scheduler
from foundations_internal.versioning import __version__
from foundations.config import set_environment
from foundations.job_parameters import *
from foundations.job_metrics import *
import foundations_internal.import_installer
import foundations_events.consumers
import foundations_events
from foundations_contrib.set_job_resources import set_job_resources
from foundations.submission import *
import foundations_core_cli

#Commented for Atlas CE
from foundations.artifacts import *
from foundations.local_run import set_up_default_environment_if_present
#Commented for Atlas CE
try:
    from foundations_orbit import *
except ModuleNotFoundError:
    pass
from foundations.set_tensorboard_logdir import set_tensorboard_logdir

def _append_module():
    import sys
    module_manager.append_module(sys.modules[__name__])


_append_module()

set_up_default_environment_if_present()

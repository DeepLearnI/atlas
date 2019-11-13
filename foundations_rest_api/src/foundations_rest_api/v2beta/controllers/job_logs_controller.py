"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

@api_resource('/api/v2beta/projects/<string:project_name>/job_listing/<string:job_id>/logs')
class JobLogsController(object):

    def index(self):
        from foundations_contrib.jobs.logs import job_logs
        try:
            logs = job_logs(self.params['job_id'])
            return Response('Jobs', LazyResult(lambda: {'log': logs}))
        except Exception as exc:
            # import traceback
            return Response('Error', LazyResult(lambda: {'message': 'Internal Server Error'}), status=500)
            # For debugging purposes:
            # just_the_string = traceback.format_exc()
            # return Response('Error', LazyResult(lambda: just_the_string), status=500)

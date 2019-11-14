"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.authentication.utils import get_token_from_header
from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

@api_resource('/api/v2beta/projects/<string:project_name>/note_listing')
class ProjectNoteListingController(object):

    def __init__(self):
        from foundations_contrib.authentication.authentication_client import AuthenticationClient
        from foundations_contrib.authentication.configs import ATLAS
        self.client = AuthenticationClient(ATLAS, '/api/v2beta/auth/login')

    def post(self):
        from foundations_contrib.global_state import redis_connection
        from foundations_internal.fast_serializer import serialize
        from datetime import datetime

        redis_connection.rpush(f'project:{self._project_name()}:note_listing', serialize({'date': datetime.now(), 'message': self._message(), 'author': self._author()}))

        return Response('Note Listing', LazyResult(lambda: f'Note with author: {self._author()} created with message: {self._message()}'))

    def _project_name(self):
        return self.params['project_name']

    def _author(self):
        return self.params['author']

    def _message(self):
        return self.params['message']

    def index(self):
        return Response('Note Listing', LazyResult(self._get_note_listing))

    def _get_note_listing(self):
        from foundations_contrib.global_state import redis_connection

        redis_note_listing_data = redis_connection.lrange(f'project:{self._project_name()}:note_listing', 0, -1)
        formatted_payload = list(map(self._format_redis_data, redis_note_listing_data))
        return formatted_payload

    def _format_redis_data(self, redis_data):
        from foundations_internal.fast_serializer import deserialize
        
        deserialized_data = deserialize(redis_data)
        author_id = deserialized_data['author']
        token = get_token_from_header()
        author_name = self.client.users_info(token)[author_id]

        return {'date': str(deserialized_data['date']), 'message': deserialized_data['message'], 'author': author_name}

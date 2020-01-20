"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_contrib.middleware_manager import MiddlewareManager
from foundations_contrib.middleware.basic_stage_middleware import BasicStageMiddleware


class TestMiddlewareManager(unittest.TestCase):

    class MockMiddleware(BasicStageMiddleware):
        pass

    class MockMiddlewareTwo(BasicStageMiddleware):
        pass

    def setUp(self):
        from foundations_internal.pipeline_context import PipelineContext
        from foundations_internal.stage_config import StageConfig
        from foundations_internal.stage_context import StageContext
        from foundations_internal.stage import Stage
        from foundations_contrib.config_manager import ConfigManager

        from uuid import uuid4

        self._pipeline_context = PipelineContext
        self._stage_config = StageConfig
        self._stage_context = StageContext

        self._stage_uuid = str(uuid4())
        self._stage = Stage(None, self._stage_uuid,
                            self._function, self._function)

        self._config_manager = ConfigManager()

    def test_has_new_cache_middleware(self):
        from foundations_contrib.middleware.new_cache_middleware import NewCacheMiddleware
        self._test_has_middleware('NewCache', NewCacheMiddleware)

    def test_has_new_cache_middleware_configured(self):
        self._test_constructor_attributes('NewCache')

    def test_has_configured_middleware(self):
        self._config_manager['stage_middleware'] = [
            {'name': 'Mock', 'constructor': self.MockMiddleware}
        ]
        self._test_has_middleware('Mock', self.MockMiddleware)

    def test_has_configured_middleware_configured(self):
        self._config_manager['stage_middleware'] = [
            {'name': 'Mock', 'constructor': self.MockMiddleware}
        ]
        self._test_constructor_attributes('Mock')

    def test_has_configured_middleware_different_middleware(self):
        self._config_manager['stage_middleware'] = [
            {'name': 'MockTwo', 'constructor': self.MockMiddlewareTwo}
        ]
        self._test_has_middleware('MockTwo', self.MockMiddlewareTwo)

    def _test_constructor_attributes(self, name):
        middleware_manager = MiddlewareManager(self._config_manager)
        middleware = self._construct_middleware(middleware_manager, name)

        # hack for ensuring construction is working
        has_any = False
        for attribute in ['_pipeline_context', '_stage_config', '_stage_context', '_stage']:
            if hasattr(middleware, attribute):
                has_any = True
                expected_result = getattr(self, attribute)
                result = getattr(middleware, attribute)
                self.assertEqual(expected_result, result)
        self.assertTrue(has_any)

    def _test_has_middleware(self, name, middleware_type):
        middleware_manager = MiddlewareManager(self._config_manager)
        middleware = self._construct_middleware(middleware_manager, name)
        self.assertTrue(isinstance(middleware, middleware_type))

    def _function(self):
        pass

    def _construct_middleware(self, middleware_manager, name):
        for middleware in middleware_manager.stage_middleware():
            if middleware.name == name:
                return middleware.callback(self._pipeline_context, self._stage_config, self._stage_context, self._stage)

        return None

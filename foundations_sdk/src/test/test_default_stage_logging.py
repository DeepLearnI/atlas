"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestDefaultStageLogging(Spec):

    class MockLoggingContext(object):

        def __init__(self):
            self.metric = None

        def log_metric(self, key, value):
            self.metric = {key: value}

    @let
    def fake_metric_name(self):
        return self.faker.word()

    @let
    def fake_metric_value(self):
        return self.faker.random.random()

    def test_stage_logging_context_defaults_to_using_global_metric_logger(self):
        mock_log_metric = self.patch('foundations_contrib.global_metric_logger.GlobalMetricLogger.log_metric')
        from foundations.stage_logging import stage_logging_context

        stage_logging_context.log_metric(self.fake_metric_name, self.fake_metric_value)
        mock_log_metric.assert_called_with(self.fake_metric_name, self.fake_metric_value)

    def test_context_is_stage_logging_context(self):
        from foundations.stage_logging import stage_logging_context
        from foundations_internal.stage_logging_context import StageLoggingContext

        self.assertTrue(isinstance(stage_logging_context, StageLoggingContext))

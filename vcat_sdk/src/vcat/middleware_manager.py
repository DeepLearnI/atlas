"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class MiddlewareManager(object):

    class NamedMiddleware(object):

        def __init__(self, name, callback):
            self.name = name
            self.callback = callback

    def __init__(self):
        self._initial_middleware = None
        self._stage_middleware = None

    def initial_middleware(self):
        if self._initial_middleware is None:
            self._initial_middleware = [
                MiddlewareManager.NamedMiddleware('Redundant', MiddlewareManager._create_redundant_middleware),
                MiddlewareManager.NamedMiddleware('Error', MiddlewareManager._create_error_middleware)
            ]

        return self._initial_middleware

    def stage_middleware(self):
        if self._stage_middleware is None:
            self._stage_middleware = [
                MiddlewareManager.NamedMiddleware('StageOutput', MiddlewareManager._create_stage_output_middleware),
                MiddlewareManager.NamedMiddleware('StageLog', MiddlewareManager._create_stage_log_middleware),
                MiddlewareManager.NamedMiddleware('ArugmentFiller', MiddlewareManager._create_argument_filler_middleware),
                MiddlewareManager.NamedMiddleware('Cache', MiddlewareManager._create_cache_middleware),
                MiddlewareManager.NamedMiddleware('UpstreamResult', MiddlewareManager._create_upstream_result_middleware),
                MiddlewareManager.NamedMiddleware('ContextAware', MiddlewareManager._create_context_aware_middleware),
                MiddlewareManager.NamedMiddleware('TimeStage', MiddlewareManager._create_time_stage_middleware),
                MiddlewareManager.NamedMiddleware('StageLogging', MiddlewareManager._create_stage_logging_middleware)
            ]

        return self._stage_middleware

    def append_initial(self, middleware):
        self.initial_middleware().append(middleware)

    def append_stage(self, middleware):
        self.stage_middleware().append(middleware)

    @staticmethod
    def _create_redundant_middleware(stage_context):
        from vcat.redundant_execution_middleware import RedundantExecutionMiddleware
        return RedundantExecutionMiddleware()

    @staticmethod
    def _create_error_middleware(stage_context):
        from vcat.error_middleware import ErrorMiddleware
        return ErrorMiddleware(stage_context)

    @staticmethod
    def _create_stage_output_middleware(pipeline_context, stage_config, stage_context, stage):
        from vcat.stage_output_middleware import StageOutputMiddleware
        return StageOutputMiddleware(pipeline_context, stage_config, stage.uuid(), stage_context)

    @staticmethod
    def _create_stage_log_middleware(pipeline_context, stage_config, stage_context, stage):
        from vcat.stage_log_middleware import StageLogMiddleware
        return StageLogMiddleware(stage_context)

    @staticmethod
    def _create_argument_filler_middleware(pipeline_context, stage_config, stage_context, stage):
        from vcat.argument_filler_middleware import ArgumentFillerMiddleware
        return ArgumentFillerMiddleware(stage)

    @staticmethod
    def _create_cache_middleware(pipeline_context, stage_config, stage_context, stage):
        from vcat.cache_middleware import CacheMiddleware
        return CacheMiddleware(stage_config, stage_context, stage.uuid())

    @staticmethod
    def _create_upstream_result_middleware(pipeline_context, stage_config, stage_context, stage):
        from vcat.upstream_result_middleware import UpstreamResultMiddleware
        return UpstreamResultMiddleware()

    @staticmethod
    def _create_context_aware_middleware(pipeline_context, stage_config, stage_context, stage):
        from vcat.context_aware_middleware import ContextAwareMiddleware
        return ContextAwareMiddleware(stage_context, stage)

    @staticmethod
    def _create_time_stage_middleware(pipeline_context, stage_config, stage_context, stage):
        from vcat.time_stage_middleware import TimeStageMiddleware
        return TimeStageMiddleware(stage_context)

    @staticmethod
    def _create_stage_logging_middleware(pipeline_context, stage_config, stage_context, stage):
        from vcat.stage_logging_middleware import StageLoggingMiddleware
        return StageLoggingMiddleware(stage)

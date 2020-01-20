"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageConnectorWrapperBuilder(object):

    def __init__(self, pipeline_context):
        from foundations_internal.stage_context import StageContext
        from foundations_internal.stage_config import StageConfig
        from foundations_internal.middleware_chain import MiddlewareChain

        self._pipeline_context = pipeline_context

        self._stage_context = StageContext()
        self._stage_config = StageConfig()

        self._middleware = MiddlewareChain()

        self._stage = None
        self._override_uuid = None
        self._connector = None

    def build(self, *additional_args):
        from foundations.stage_connector_wrapper import StageConnectorWrapper

        return StageConnectorWrapper(self._stage, self._pipeline_context, self._stage_context, self._stage_config)

    def uuid(self, uuid):
        self._override_uuid = uuid
        return self

    def hierarchy(self, parent_uuids):
        stage_hierarchy = self._pipeline_context.provenance.stage_hierarchy
        stage_hierarchy.add_entry(self._stage, parent_uuids)

        return self

    def stage(self, current_uuid, function, args, kwargs):
        from foundations_internal.stage import Stage

        new_args = self._new_arguments(args)
        new_args += self._new_keyword_arguments(kwargs)

        stage_uuid = self._override_uuid or self._make_uuid(current_uuid, function, new_args, {})
        self._stage_context.uuid = stage_uuid
        self._stage = Stage(self._middleware, stage_uuid,
                            function, function, *new_args)
        return self

    def _new_arguments(self, args):
        from foundations_internal.argument import Argument

        return tuple(Argument.generate_from(argument, None)
                     for argument in args)

    def _new_keyword_arguments(self, kwargs):
        from foundations_internal.argument import Argument

        kwarg_keys = list(kwargs.keys())
        kwarg_keys.sort()

        new_kwargs = [(key, kwargs[key]) for key in kwarg_keys]
        return tuple(Argument.generate_from(argument, keyword)
                     for keyword, argument in new_kwargs)

    def _uuid(self):
        return self._stage.uuid()

    def _make_uuid(self, current_uuid, function, args, kwargs):
        from foundations.argument_hasher import ArgumentHasher
        from foundations.utils import merged_uuids

        argument_hasher = ArgumentHasher(args, kwargs)
        argument_uuid = argument_hasher.make_hash()
        function_uuid = self._function_hash(function)
        return merged_uuids([current_uuid, function_uuid, argument_uuid])

    def _function_hash(self, function):
        from foundations.utils import generate_uuid
        from foundations.utils import merged_uuids
        from foundations_internal.safe_inspect import getsource

        name_uuid = generate_uuid(function.__name__)
        source_uuid = generate_uuid(getsource(function))

        return merged_uuids([name_uuid, source_uuid])

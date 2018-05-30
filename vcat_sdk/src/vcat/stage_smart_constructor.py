from vcat.stage import Stage
from vcat.utils import merged_uuids
from vcat.argument_hasher import ArgumentHasher


class StageSmartConstructor(object):

    def __init__(self, stage_context):
        self._stage_context = stage_context

    def make_stage(self, current_uuid, stage_context, function, *args, **kwargs):
        stage_uuid = self._make_uuid(current_uuid, function, args, kwargs)
        stage_context.uuid = stage_uuid
        return Stage(stage_uuid, self._wrapped_function(stage_uuid, function), function, *args, **kwargs)

    def _make_uuid(self, current_uuid, function, args, kwargs):
        argument_hasher = ArgumentHasher(args, kwargs)
        argument_uuid = argument_hasher.make_hash()
        return merged_uuids([current_uuid, function.__name__, argument_uuid])

    def _wrapped_function(self, stage_uuid, function):
        def wrapped(*args, **kwargs):
            import time

            start_time = time.time()
            stage_output = function(*args, **kwargs)
            end_time = time.time()
            if isinstance(stage_output, tuple):
                return_value, result = stage_output
                self._stage_context.stage_log = result
            else:
                return_value = stage_output
            self._stage_context.start_time = start_time
            self._stage_context.end_time = end_time
            self._stage_context.delta_time = end_time - start_time
            return return_value
        return wrapped

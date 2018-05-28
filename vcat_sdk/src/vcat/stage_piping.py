class StagePiping(object):

    def __init__(self, pipe):
        self._pipe = pipe

    def pipe(self, stage_args):
        if isinstance(stage_args, tuple):
            function = stage_args[0]
            args = list(stage_args[1:])
            last_argument = args[-1]
            if isinstance(last_argument, dict):
                kwargs = last_argument
                args.pop()
                return self._pipe.stage(function, *args, **kwargs)
            else:
                return self._pipe.stage(function, *args)
        else:
            if callable(stage_args):
                function = stage_args
            else:
                def constant():
                    return stage_args
                function = constant

            return self._pipe.stage(function)

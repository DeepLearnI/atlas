# TODO: remove
class PipelineExecutor(object):
  def __init__(self, pipeline_context):
    self.pipeline_context = pipeline_context

  def execute(self, stage_function, *args, **kwargs):
    self.pipeline_context.results.update(kwargs)
    return stage_function(self.pipeline_context, *args, **kwargs)



# UGLY (DEVS)
class Stage(object):

  def __init__(self, function, *args, **kwargs):
    import uuid
    self.uuid = uuid.uuid4()

    self.function = function
    self.args = args
    self.kwargs = kwargs
  
  def run(self, *local_args):
    return self.function(*(local_args + self.args), **self.kwargs)
  
  def name(self):
    return str(self.uuid)

  def function_name(self):
    return self.function.__name__
  
class StageConnector(object):
  def __init__(self, current_stage, previous_connectors):
    self._current_stage = current_stage
    self._previous_connectors = previous_connectors
  
  def name(self):
    return self._current_stage.name()

  def function_name(self):
    return self._current_stage.function_name()

  def args(self):
    return self._current_stage.args

  def kwargs(self):
    return self._current_stage.kwargs

  def tree_names(self):
    parent_trees = [connector.tree_names() for connector in self._previous_connectors]
    return {"stage": self.name(), "function_name": self.function_name(), "args": self.args(), "kwargs": self.kwargs(), "parents": parent_trees}
      
  def stage(self, next_stage):
    return StageConnector(next_stage, [self])
  
  def run(self, *args, **kwargs):
    previous_results = [connector.run() for connector in self._previous_connectors]
    list_args = list(args)
    return self._current_stage.run(*(previous_results + list_args), **kwargs)

  def serialize(self):
    import dill as pickle
    return pickle.dumps(self)
  
  @staticmethod
  def deserialize(serialized_self):
    import dill as pickle
    return pickle.loads(serialized_self)


class StageGraph(object):
  def stage(self, stage):
    return StageConnector(stage, [])
  
  def join(self, stage, upstream_connectors):
    return StageConnector(stage, upstream_connectors)

# PRETTY (ERIC)
class StageConnectorWrapper(object):
  def __init__(self, connector, pipeline_context):
    self._connector = connector
    self._pipeline_context = pipeline_context

  def tree_names(self):
    return self._connector.tree_names()
        
  def stage(self, function, *args, **kwargs):
    return StageConnectorWrapper(self._connector.stage(self._make_stage(function, *args, **kwargs)), self._pipeline_context)
  
  def __or__(self, stage_args):
    if isinstance(stage_args, tuple):
      function = stage_args[0]
      args = list(stage_args[1:])
      last_argument = args[-1]
      if isinstance(last_argument, dict):
        kwargs = last_argument
        args.pop()
        return self.stage(function, *args, **kwargs)
      else:
        return self.stage(function, *args)
    else:
      return self.stage(stage_args)

  def run(self, *args, **kwargs):
    return self._connector.run(*args, **kwargs)
  
  def __call__(self, *args, **kwargs):
    return self.run(*args, **kwargs)

  def _make_stage(self, function, *args, **kwargs):
    return Stage(self._wrapped_function(function), *args, **kwargs)

  def _wrapped_function(self, function):
    def wrapped(*args, **kwargs):
      stage_output = function(*args, **kwargs)
      if isinstance(stage_output, tuple):
        return_value, result = stage_output
        self._pipeline_context.results.update(result)
      else:
        return_value = stage_output
      return return_value
    return wrapped    

  def serialize(self):
    return self._connector.serialize()
  
  @staticmethod
  def deserialize(serialized_self):
    return StageConnectorWrapper(StageConnector.deserialize(serialized_self))

  
class Pipeline(object):
  def __init__(self, pipeline_context):
    self.graph = StageGraph()
    self.pipeline_context = pipeline_context
      
  def stage(self, function, *args, **kwargs):
    current_stage = self._make_stage(function, *args, **kwargs)
    return StageConnectorWrapper(self.graph.stage(current_stage), self.pipeline_context)
  
  def join(self, upstream_connector_wrappers, function, *args, **kwargs):
    upstream_connectors = [wrapper._connector for wrapper in upstream_connector_wrappers]
    current_stage = self._make_stage(function, *args, **kwargs)
    return StageConnectorWrapper(self.graph.join(current_stage, upstream_connectors), self.pipeline_context)
  
  def _make_stage(self, function, *args, **kwargs):
    return Stage(self._wrapped_function(function), *args, **kwargs)

  def _wrapped_function(self, function):
    def wrapped(*args, **kwargs):
      stage_output = function(*args, **kwargs)
      if isinstance(stage_output, tuple):
        return_value, result = stage_output
        self.pipeline_context.results.update(result)
      else:
        return_value = stage_output
      return return_value
    return wrapped    

  def __or__(self, stage_args):
    if isinstance(stage_args, tuple):
      function = stage_args[0]
      args = list(stage_args[1:])
      last_argument = args[-1]
      if isinstance(last_argument, dict):
        kwargs = last_argument
        args.pop()
        return self.stage(function, *args, **kwargs)
      else:
        return self.stage(function, *args)
    else:
      return self.stage(stage_args)  

# PRETTY (BUT NOT ERIC)
class PipelineContext(object):

  def __init__(self):
    import uuid

    self.results = {}
    self.predictions = {}
    self.file_name = str(uuid.uuid4()) + ".json"

  # TODO: can remove
  def simple_stage(self, stage_function, *args, **kwargs):
    return PipelineExecutor(self).execute(stage_function, *args, **kwargs)

  # TODO: can remove
  def stage(self, stage_function, *args, **kwargs):
    def executor_function(pipeline_context, *args, **kwargs):
      stage_output = stage_function(*args, **kwargs)
      if isinstance(stage_output, tuple):
        return_value, result = stage_output
        self.results.update(result)
      else:
        return_value = stage_output
      return return_value

    return PipelineExecutor(self).execute(executor_function, *args, **kwargs)

  def save(self, result_saver):
    result_saver.save(self.file_name, self.results)

class RedisResultSaver(object):
  def __init__(self):
    import redis

    self._connection = redis.Redis()

  def save(self, name, results):
    import json

    results_serialized = json.dumps(results)
    self._connection.sadd("result_names", name)
    self._connection.set("results:" + name, results_serialized)

class ResultReader(object):
  
  def __init__(self):
    # import glob
    # import json

    # self.results = []
    # file_list = glob.glob('*.json')
    # for file_name in file_list:
    #   with open(file_name) as file:
    #     self.results.append(json.load(file))

    self.results = RedisFetcher().fetch_results()
  
  def to_pandas(self):
    import pandas
    return pandas.DataFrame(self.results)

class RedisFetcher(object):
  def __init__(self):
    import redis

    self._connection = redis.Redis()

  def fetch_results(self):
    import json

    result_names = self._connection.smembers("result_names")
    result_keys = ["results:" + name.decode("utf-8") for name in result_names]
    results_serialized = [self._connection.get(key) for key in result_keys]
    return [json.loads(result_serialized) for result_serialized in results_serialized]


pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)
from os.path import join

def translate(config):
    from foundations_contrib.helpers.shell import find_bash
    from foundations_contrib.config.mixin import ssh_configuration
    from jsonschema import validate
    import foundations_contrib
    import yaml

    with open(f'{foundations_contrib.root()}/resources/config_validation/submission.yaml') as file:
        schema = yaml.load(file.read())
    validate(instance=config, schema=schema)

    result = {
        'deployment_implementation': _deployment_implementation(),
        'redis_url': _redis_url(config),
        'shell_command': find_bash(),
        'obfuscate_foundations': _obfuscate_foundations(config),
        'worker_container_overrides': config.get('worker', {})
    }
    if not 'host' in config['ssh_config']:
        config['ssh_config']['host'] = _kubernetes_master_ip()
    result.update(ssh_configuration(config))

    return result 

def _kubernetes_master_ip():
    import subprocess
    import yaml

    node_yaml = subprocess.check_output(['kubectl', 'get', 'node', '-o', 'yaml', '-l', 'node-role.kubernetes.io/master='])
    node = yaml.load(node_yaml)
    return node['items'][0]['status']['addresses'][0]['address']

def _redis_url(config):
    return config['results_config'].get('redis_end_point', 'redis://localhost:6379')

def _deployment_implementation():
    from foundations_scheduler_plugin.job_deployment import JobDeployment
    return {
        'deployment_type': JobDeployment
    }

def _obfuscate_foundations(config):
    return config.get('obfuscate_foundations', False)
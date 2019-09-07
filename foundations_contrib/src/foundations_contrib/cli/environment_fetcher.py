"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class EnvironmentFetcher(object):
    """
    Checks the local and global config locations for environments
    """

    def __init__(self):
        pass
    
    def get_all_environments(self):
        local_environments = self._get_local_environments()
        global_environments = self._get_global_environments()

        return local_environments, global_environments
    
    def find_environment(self, env_name):
        file_name = '{}.{}'.format(env_name, 'config.yaml')
        local_environments = self._get_local_environments()

        if local_environments == None:
            local_environments = []
        global_environments = self._get_global_environments()
        all_environments = local_environments + global_environments
        return list(self._environments_with_name(all_environments, file_name))

    def _environments_with_name(self, environments, environment_file_name):
        import os.path

        for environment in environments:
            if environment_file_name == os.path.basename(environment):
                yield environment

    def _get_local_environments(self):
        import os
        from glob import glob

        cwd = os.getcwd()
        directories = os.listdir()

        if 'config' not in directories:
            return None

        config_directory = os.path.join(cwd, 'config', 'execution', '*.config.yaml')
        return glob(config_directory)
        
    
    def _get_global_environments(self):
        from glob import glob
        from os.path import expanduser, join
        from foundations_contrib.utils import foundations_home
        # TODO: Add /submission to global_config_directory
        global_config_directory = expanduser(foundations_home() + '/config/submission')
        search_path = join(global_config_directory, '*.config.yaml')
        return glob(search_path)

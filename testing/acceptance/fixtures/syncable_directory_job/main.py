"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations

print(foundations.config_manager.config())

first_directory = foundations.create_syncable_directory('some data', 'results')
first_directory.upload()

second_directory = foundations.create_syncable_directory('some metadata', 'metadata')
second_directory.upload()
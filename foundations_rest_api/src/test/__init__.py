"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import os

os.environ['TZ'] = 'EST'

from test.test_global_state import TestGlobalState
from test.utils import *
from test.v1 import *
from test.v2beta import *
from test.filters import *

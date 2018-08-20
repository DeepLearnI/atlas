"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.constant_parameter import ConstantParameter
from foundations.basic_stage_middleware import BasicStageMiddleware


class TestConstantParameter(unittest.TestCase):

    def test_stores_value(self):
        parameter = ConstantParameter('world')
        self.assertEqual('world', parameter.compute_value(None))

    def test_stores_value_different_value(self):
        parameter = ConstantParameter('potato')
        self.assertEqual('potato', parameter.compute_value(None))

    def test_value_hash(self):
        parameter = ConstantParameter('potato')
        self.assertEqual(
            '3e2e95f5ad970eadfa7e17eaf73da97024aa5359', parameter.hash(None))

    def test_value_hash_different_value(self):
        parameter = ConstantParameter('mashed potato')
        self.assertEqual(
            '321e42b16eff1d6695a97ed82dc8b24f455db67d', parameter.hash(None))

    def test_has_enable_caching_method(self):
        parameter = ConstantParameter('mashed potato')
        parameter.enable_caching()

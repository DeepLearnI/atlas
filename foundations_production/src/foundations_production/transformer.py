"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Transformer(object):
    
    def __init__(self, user_transformer_class, list_of_columns=None):
        from foundations_production.base_transformer import BaseTransformer
        from foundations_production.preprocessor_class import Preprocessor
        from foundations_production.persister import Persister
        from foundations_production import model_package

        self._columns = list_of_columns
        self._base_transformer = BaseTransformer(Preprocessor.active_preprocessor, Persister(model_package), user_transformer_class())

    def fit(self, data):
        self._base_transformer.fit(self._column_data(data))

    def transform(self, data):
        return self._base_transformer.transformed_data(self._column_data(data))

    def _column_data(self, data):
        if self._columns is not None:
            return data[self._columns]
        else:
            return data

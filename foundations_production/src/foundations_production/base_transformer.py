"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import foundations
from foundations_production.persister import Persister

class BaseTransformer(object):

    class State(object):

        def __init__(self, should_load, transformer_index):
            self._should_load = should_load
            self._transformer_index = transformer_index
        
        @property
        def should_load(self):
            return self._should_load
        
        @should_load.setter
        def should_load(self, value):
            self._should_load = value

        @property
        def transformer_index(self):
            return self._transformer_index
        
        @transformer_index.setter
        def transformer_index(self, value):
            self._transformer_index = value
             
        def fit_stage(self, persister, user_defined_transformer, *args, **kwargs):
            if self.should_load:
                return self._loaded_transformer(persister)
            return self._fitted_transformer(persister, user_defined_transformer, *args, **kwargs)
        
        def _loaded_transformer(self, persister):
            return persister.load_user_defined_transformer(self.transformer_index)

        def _fitted_transformer(self, persister, user_defined_transformer, *args, **kwargs):
            user_defined_transformer.fit(*args, **kwargs)
            persister.save_user_defined_transformer(self.transformer_index, user_defined_transformer)
            return user_defined_transformer

    def __init__(self, preprocessor, user_defined_transformer):
        self._encoder = None
        self._user_defined_transformer = user_defined_transformer

        self._persister_stage = foundations.create_stage(self._create_persister)(job_id=preprocessor.job_id)
        self._state = self.State(should_load=False, transformer_index=preprocessor.new_transformer(self))

    def fit(self, *args, **kwargs):
        if self._encoder is None:
            self._encoder = foundations.create_stage(self._state.fit_stage)(self._persister_stage, self._user_defined_transformer, *args, **kwargs)

    def encoder(self):
        if self._encoder is not None:
            return self._encoder
        raise ValueError('Transformer has not been fit. Call #fit() before using with encoder.')
    
    def transformed_data(self, *args, **kwargs):
        return foundations.create_stage(self._user_defined_transformer_stage)(self.encoder(), *args, **kwargs)

    def load(self):
        self._state.should_load = True

    @staticmethod
    def _create_persister(job_id):
        return Persister(job_id)

    @staticmethod
    def _user_defined_transformer_stage(user_defined_transformer, *args, **kwargs):
        return user_defined_transformer.transform(*args, **kwargs)
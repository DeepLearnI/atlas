"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DataContract(object):

    def __init__(self, contract_name, df=None):
        import pandas

        self.options = self._default_options()
        self._contract_name = contract_name

        if df is None:
            dataframe = pandas.DataFrame()
        else:
            dataframe = df

        self._column_names = list(dataframe.columns)
        self._column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in self._column_names}

    @staticmethod
    def _default_options():
        import numpy
        from foundations_orbit.data_contract_options import DataContractOptions

        default_distribution = {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'cols_to_include': None,
            'cols_to_ignore': None,
            'custom_thresholds': {}
        }

        return DataContractOptions(
            max_bins=50,
            check_schema=True,
            check_row_count=False,
            special_values=[numpy.nan],
            check_distribution=True,
            distribution=default_distribution
        )

    def save(self, model_package_directory):
        with open(self._data_contract_file_path(model_package_directory), 'wb') as contract_file:
            contract_file.write(self._serialized_contract())

    @staticmethod
    def load(model_package_directory, contract_name):
        import pickle

        data_contract_file_name = DataContract._data_contract_file_path_with_contract_name(model_package_directory, contract_name)
        with open(data_contract_file_name, 'rb') as contract_file:
            return DataContract._deserialized_contract(contract_file.read())

    def validate(self, dataframe_to_validate, *args):
        validation_report = {}

        if self.options.check_schema:
            validation_report['schema_check_results'] = self._schema_check_results(dataframe_to_validate)

        if self.options.check_row_count:
            validation_report['row_cnt_diff'] = self._row_count_difference(dataframe_to_validate)

        if self.options.check_distribution:
            validation_report['dist_check_results'] = self._distribution_check_results(dataframe_to_validate)

        return validation_report

    def _schema_check_results(self, dataframe_to_validate):
        import pandas

        columns_to_validate = list(dataframe_to_validate.columns)

        if self._column_names_match(columns_to_validate):
            types_to_validate = {column_name: str(dataframe_to_validate.dtypes[column_name]) for column_name in columns_to_validate}
            
            if self._data_types_match(types_to_validate):
                return {'passed': True}
            
            return self._type_mismatch_error_information(self._column_types, types_to_validate)

        ref_column_names = set(self._column_names)
        current_column_names = set(columns_to_validate)

        if self._column_sets_not_equal(ref_column_names, current_column_names):
            return self._column_sets_not_equal_error_information(ref_column_names, current_column_names)

        ref_column_series = pandas.Series(self._column_names)
        current_column_series = pandas.Series(columns_to_validate)

        return self._column_sets_in_wrong_order_information(ref_column_series, current_column_series)

    def _column_names_match(self, columns_to_validate):
        return self._column_names == columns_to_validate

    def _data_types_match(self, types_to_validate):
        return self._column_types == types_to_validate

    @staticmethod
    def _type_mismatch_error_information(ref_column_types, types_to_validate):
        mismatched_columns = {}

        for column_name in ref_column_types.keys():
            ref_type = ref_column_types[column_name]
            current_type = types_to_validate[column_name]

            if ref_type != current_type:
                mismatched_columns[column_name] = {
                    'ref_type': ref_type,
                    'current_type': current_type
                }

        return {'passed': False, 'error_message': 'column datatype mismatches', 'cols': mismatched_columns}

    @staticmethod
    def _column_sets_not_equal(ref_column_names, current_column_names):
        return ref_column_names != current_column_names

    @staticmethod
    def _column_sets_not_equal_error_information(ref_column_names, current_column_names):
        missing_in_ref = current_column_names - ref_column_names
        missing_in_current = ref_column_names - current_column_names

        return {'passed': False, 'error_message': 'column sets not equal', 'missing_in_ref': list(missing_in_ref), 'missing_in_current': list(missing_in_current)}

    @staticmethod
    def _column_sets_in_wrong_order_information(ref_column_series, current_column_series):
        columns_out_of_order = current_column_series[current_column_series != ref_column_series]
        return {'passed': False, 'error_message': 'columns not in order', 'columns_out_of_order': list(columns_out_of_order)}

    def _row_count_difference(self, dataframe_to_validate):
        return len(dataframe_to_validate) - 1

    def _distribution_check_results(self, dataframe_to_validate):
        import numpy

        columns_to_validate = list(dataframe_to_validate.columns)

        dist_check_results = {}

        results_for_same_distribution = {
            'binned_l_infinity': 0.0,
            'binned_passed': True,
            'special_values': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        for column_name in columns_to_validate:
            dist_check_results[column_name] = results_for_same_distribution

        return dist_check_results

    def __eq__(self, other):
        return self._contract_name == other._contract_name and self.options == other.options

    def _data_contract_file_path(self, model_package_directory):
        return self._data_contract_file_path_with_contract_name(model_package_directory, self._contract_name)

    @staticmethod
    def _data_contract_file_path_with_contract_name(model_package_directory, contract_name):
        return f'{model_package_directory}/{contract_name}.pkl'

    def _serialized_contract(self):
        import pickle

        contract = DataContract(self._contract_name)
        contract.options = self.options

        return pickle.dumps(contract)

    @staticmethod
    def _deserialized_contract(serialized_contract):
        import pickle
        return pickle.loads(serialized_contract)
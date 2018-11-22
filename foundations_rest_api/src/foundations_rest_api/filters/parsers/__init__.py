"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from foundations_rest_api.filters.parsers.datetime_parser import DateTimeParser
from foundations_rest_api.filters.parsers.elapsedtime_parser import ElapsedTimeParser
from foundations_rest_api.filters.parsers.status_parser import StatusParser
from foundations_rest_api.filters.parsers.string_parser import StringParser


DATE_TIME, ELAPSED_TIME, STATUS, STRING = range(1, 5)


_column_type_parser = {
    DATE_TIME: DateTimeParser,
    ELAPSED_TIME: ElapsedTimeParser,
    STATUS: StatusParser,
    STRING: StringParser,
}


_column_type = {
    'job_id': STRING,
    'duration': ELAPSED_TIME,
    'submitted_time': DATE_TIME,
    'start_time': DATE_TIME,
    'completed_time': DATE_TIME,
    'user': STRING,
    'status': STATUS,
}


def get_parser(column_name):
    return _column_type_parser[_column_type[column_name]]()

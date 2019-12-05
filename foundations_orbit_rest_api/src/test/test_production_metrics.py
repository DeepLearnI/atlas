"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.production_metrics import all_production_metrics

class TestProductionMetrics(Spec):
    
    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let_now
    def environ(self):
        fake_environ = {}
        fake_environ['MONITOR_NAME'] = self.monitor_name
        fake_environ['PROJECT_NAME'] = self.project_name
        return self.patch('os.environ', fake_environ)

    @tear_down
    def tear_down(self):
        self.redis_connection.flushall()

    @let
    def monitor_name(self):
        return self.faker.uuid4()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def metric_name(self):
        return self.faker.word()

    @let
    def metric_column(self):
        return self.faker.word()

    @let
    def metric_value(self):
        return self.faker.random.random()

    @let
    def metric_name_2(self):
        return self.faker.word()

    @let
    def metric_column_2(self):
        return self.faker.word()

    @let
    def metric_value_2(self):
        return self.faker.random.random()

    @set_up
    def set_up(self):
        self.redis_connection.flushall()

    def test_all_production_metrics_returns_empty_dictionary_if_job_not_in_redis(self):
        self.assertEqual({}, all_production_metrics(self.project_name, self.monitor_name))

    def test_all_production_metrics_returns_dictionary_with_one_entry_whose_value_empty_list_when_metrics_dict_is_empty(self):
        from foundations_orbit import track_production_metrics

        track_production_metrics(self.metric_name, {})

        expected_tracked_metrics = {self.metric_name: []}
        self.assertEqual(expected_tracked_metrics, all_production_metrics(self.project_name, self.monitor_name))

    def test_all_production_metrics_returns_dictionary_with_one_entry_whose_value_is_singleton_list_with_key_value_pair_when_metric_logged_with_one_value(self):
        from foundations_orbit import track_production_metrics

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value})

        expected_tracked_metrics = {self.metric_name: [(self.metric_column, self.metric_value)]}
        self.assertEqual(expected_tracked_metrics, all_production_metrics(self.project_name, self.monitor_name))

    def test_all_production_metrics_returns_dictionary_with_one_entry_whose_value_is_list_with_key_value_pairs_when_metrics_logged(self):
        from foundations_orbit import track_production_metrics

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value, self.metric_column_2: self.metric_value_2})

        expected_tracked_metrics = {self.metric_name: [(self.metric_column, self.metric_value), (self.metric_column_2, self.metric_value_2)]}
        self.assertEqual(expected_tracked_metrics, all_production_metrics(self.project_name, self.monitor_name))

    def test_all_production_metrics_returns_dictionary_with_all_entries_when_multiple_metrics_tracked(self):
        from foundations_orbit import track_production_metrics

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value})
        track_production_metrics(self.metric_name_2, {self.metric_column_2: self.metric_value_2})

        expected_tracked_metrics = {
            self.metric_name: [(self.metric_column, self.metric_value)],
            self.metric_name_2: [(self.metric_column_2, self.metric_value_2)]
        }

        self.assertEqual(expected_tracked_metrics, all_production_metrics(self.project_name, self.monitor_name))
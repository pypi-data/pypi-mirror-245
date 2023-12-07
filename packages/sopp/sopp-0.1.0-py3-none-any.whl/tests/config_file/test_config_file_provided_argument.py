from datetime import datetime
from pathlib import Path

import pytest
import pytz

from sopp.config_file.config_file_factory import get_config_file_object
from sopp.config_file.support.config_file_base import ConfigFileBase
from sopp.custom_dataclasses.configuration import Configuration
from sopp.custom_dataclasses.coordinates import Coordinates
from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from sopp.custom_dataclasses.observation_target import ObservationTarget
from sopp.custom_dataclasses.position import Position
from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.custom_dataclasses.runtime_settings import RuntimeSettings
from sopp.utilities import get_script_directory


class TestConfigFileProvidedArgument:
    @pytest.fixture(params=['config_file_json/arbitrary_config_file.json'])
    def config_arbitrary(self, request):
        yield self._get_config_file_object(config_filename=request.param)

    def test_reads_inputs_of_provided_config_file_correctly(self, config_arbitrary):
        assert config_arbitrary.configuration == Configuration(
            reservation=Reservation(
                facility=Facility(
                    coordinates=Coordinates(latitude=40.8178049,
                                            longitude=-121.4695413),
                    name='ARBITRARY_1',
                    elevation=1000,
                ),
                time=TimeWindow(begin=datetime(year=2023, month=3, day=30, hour=10, tzinfo=pytz.UTC),
                                end=datetime(year=2023, month=3, day=30, hour=11, tzinfo=pytz.UTC)),
                frequency=FrequencyRange(
                    frequency=135,
                    bandwidth=10
                )
            ),
            antenna_position_times=None,
            observation_target=ObservationTarget(declination='-38d6m50.8s', right_ascension='4h42m'),
            static_antenna_position=Position(altitude=.2, azimuth=.3),
        )

    def test_json_allows_antenna_position_times(self):
        config = self._get_config_file_object(config_filename='config_file_json/arbitrary_config_file_with_antenna_position_times.json')
        assert config.configuration.antenna_position_times == [
            PositionTime(position=Position(altitude=.0, azimuth=.1),
                         time=datetime(year=2023, month=3, day=30, hour=10, minute=1, tzinfo=pytz.UTC)),
            PositionTime(position=Position(altitude=.1, azimuth=.2),
                         time=datetime(year=2023, month=3, day=30, hour=10, minute=2, tzinfo=pytz.UTC))
        ]

    def test_json_runtime_settings(self):
        config = self._get_config_file_object(config_filename='config_file_json/arbitrary_config_file_runtime_settings.json')
        expected = RuntimeSettings(time_continuity_resolution=5, concurrency_level=6)
        actual = config.configuration.runtime_settings
        assert expected == actual

    @pytest.fixture(params=['config_file_json/arbitrary_config_file_no_observation_target.json'])
    def config_no_observation_target(self, request):
        yield self._get_config_file_object(config_filename=request.param)
    def test_observation_target_is_optional(self, config_no_observation_target):
        assert config_no_observation_target.configuration.observation_target is None
        assert config_no_observation_target.configuration.reservation is not None
        assert config_no_observation_target.configuration.static_antenna_position is not None

    @pytest.fixture(params=['config_file_json/arbitrary_config_file_partial_observation_target.json'])
    def config_partial_observation_target(self, request):
        yield self._get_config_file_object(config_filename=request.param)
    def test_error_is_returned_if_partial_observation_target(self, config_partial_observation_target):
        with pytest.raises(KeyError):
            _ = config_partial_observation_target.configuration

    @pytest.fixture(params=['config_file_json/arbitrary_config_file_no_static_antenna_position.json'])
    def config_no_static_antenna_position(self, request):
        yield self._get_config_file_object(config_filename=request.param)
    def test_static_antenna_position_is_optional(self, config_no_static_antenna_position):
        assert config_no_static_antenna_position.configuration.static_antenna_position is None
        assert config_no_static_antenna_position.configuration.observation_target is not None
        assert config_no_static_antenna_position.configuration.reservation is not None

    @pytest.fixture(params=['config_file_json/arbitrary_config_file_partial_static_antenna_position.json'])
    def config_partial_static_antenna_position(self, request):
        yield self._get_config_file_object(config_filename=request.param)
    def test_error_is_returned_if_partial_static_antenna_position(self, config_partial_static_antenna_position):
        with pytest.raises(KeyError):
            _ = config_partial_static_antenna_position.configuration

    @staticmethod
    def _get_config_file_object(config_filename: str) -> ConfigFileBase:
        return get_config_file_object(config_filepath=Path(get_script_directory(__file__), config_filename))

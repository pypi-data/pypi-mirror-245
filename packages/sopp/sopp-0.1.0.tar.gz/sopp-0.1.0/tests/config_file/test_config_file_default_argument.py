import os
import shutil
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
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.utilities import CONFIG_FILE_FILENAME, CONFIG_FILE_FILENAME_JSON, default_config_filepaths, \
    get_script_directory, get_supplements_directory


class TestConfigFileDefaultArgument:
    @pytest.fixture(scope='class')
    def backup_current_default_config_file(self):
        default_filepaths = default_config_filepaths()
        backup_filepaths = {default_filepath: Path(f'{default_filepath}.bak') for default_filepath in default_filepaths}

        for default_filepath, backup_filepath in backup_filepaths.items():
            if default_filepath.exists():
                os.rename(default_filepath, backup_filepath)

        yield

        for default_filepath, backup_filepath in backup_filepaths.items():
            if backup_filepath.exists():
                os.rename(backup_filepath, default_filepath)

    @pytest.fixture(scope='class', params=[('config_file_json/arbitrary_config_file_2.json', CONFIG_FILE_FILENAME_JSON)])
    def config_file(self, request, backup_current_default_config_file):
        source_relative_filepath, target_filename = request.param
        supplements_directory = get_supplements_directory()
        source_filepath = Path(get_script_directory(__file__), source_relative_filepath)
        target_filepath = Path(supplements_directory, target_filename)

        os.makedirs(supplements_directory, exist_ok=True)
        shutil.copyfile(source_filepath, target_filepath)

        yield get_config_file_object()

        target_filepath.unlink(missing_ok=True)

    def test_reads_inputs_of_provided_config_file_correctly(self, config_file):
        assert config_file.configuration == Configuration(
            reservation=Reservation(
                facility=Facility(
                    coordinates=Coordinates(latitude=40.8178049,
                                            longitude=-121.4695413),
                    name='ARBITRARY_2',
                    elevation=1000,
                ),
                time=TimeWindow(begin=datetime(year=2023, month=3, day=30, hour=10, tzinfo=pytz.UTC),
                                end=datetime(year=2023, month=3, day=30, hour=11, tzinfo=pytz.UTC)),
                frequency=FrequencyRange(
                    frequency=135,
                    bandwidth=10
                )
            ),
            observation_target=ObservationTarget(declination='-38d6m50.8s', right_ascension='4h42m'),
            static_antenna_position=Position(altitude=.2, azimuth=.3)
        )

from sopp.custom_dataclasses.observation_target import ObservationTarget
from sopp.custom_dataclasses.facility import Facility
from sopp.custom_dataclasses.coordinates import Coordinates
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.runtime_settings import RuntimeSettings
from sopp.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from sopp.path_finder.observation_path_finder_rhodesmill import ObservationPathFinderRhodesmill
from sopp.frequency_filter.frequency_filter import FrequencyFilter
from sopp.satellites_loader.satellites_loader_from_files import SatellitesLoaderFromFiles
from sopp.config_file.config_file_factory import get_config_file_object

from typing import Optional
from datetime import datetime, timedelta


class ConfigurationBuilder:
    def __init__(self):
        self._facility = None
        self._time_window = None
        self._frequency_range = None
        self._observation_target = None

        self.antenna_direction_path = None
        self.satellites = None
        self.reservation = None
        self.runtime_settings = RuntimeSettings()

    def set_facility(self,
            latitude: float,
            longitude: float,
            elevation: float,
            name: str,
            beamwidth: float,
            bandwidth: float,
            frequency: float,
        ):
        self._facility = Facility(
            Coordinates(latitude=latitude, longitude=longitude),
            elevation=elevation,
            beamwidth=beamwidth,
            name=name,
        )
        self._frequency_range = FrequencyRange(
            bandwidth=bandwidth,
            frequency=frequency,
        )
        return self

    def set_time_window(self, begin: datetime, end: datetime):
        self._time_window = TimeWindow(
            begin=begin,
            end=end,
        )
        return self

    def set_observation_target(self, declination: str, right_ascension: str):
        self._observation_target = ObservationTarget(
            declination=declination,
            right_ascension=right_ascension,
        )
        return self

    def set_satellites(self, tle_file: str, frequency_file: Optional[str] = None):
        self.satellites = SatellitesLoaderFromFiles(
            tle_file=tle_file,
            frequency_file=frequency_file,
        ).load_satellites()
        return self

    def set_runtime_settings(self, concurrency_level: int, time_continuity_resolution: int):
        self.runtime_settings = RuntimeSettings(
            concurrency_level=concurrency_level,
            time_continuity_resolution=time_continuity_resolution,
        )
        return self

    def set_config_file(self, config_file: str):
        config = get_config_file_object(config_filepath=config_file).configuration
        self._frequency_range = config.reservation.frequency
        self._facility = config.reservation.facility
        self._time_window = config.reservation.time
        self._observation_target = config.observation_target
        self.runtime_settings = config.runtime_settings
        return self

    def _frequency_filter_satellites(self):
        self.satellites = FrequencyFilter(
            satellites=self.satellites,
            observation_frequency=self._frequency_range
        ).filter_frequencies()

    def _build_reservation(self):
        self.reservation = Reservation(
            facility=self._facility,
            time=self._time_window,
            frequency=self._frequency_range
        )

    def _build_antenna_direction_path(self):
        if self._observation_target is not None:
            self.antenna_direction_path = ObservationPathFinderRhodesmill(
                self._facility,
                self._observation_target,
                self._time_window
            ).calculate_path()

    def build(self):
        if not all(
            [self._facility, self._time_window, self._frequency_range,
             self._observation_target, self.satellites]
        ):
            raise ValueError("Incomplete configuration. Please set all required parameters.")

        self._frequency_filter_satellites()
        self._build_antenna_direction_path()
        self._build_reservation()

        return self

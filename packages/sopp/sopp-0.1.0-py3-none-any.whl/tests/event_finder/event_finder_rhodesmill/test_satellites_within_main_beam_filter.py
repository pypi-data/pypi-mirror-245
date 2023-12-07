from dataclasses import replace
from datetime import datetime, timedelta
from typing import Optional

import pytz

from sopp.custom_dataclasses.position_time import PositionTime
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.event_finder.event_finder_rhodesmill.support.satellites_within_main_beam_filter import SatellitesWithinMainBeamFilter, \
    AntennaPosition
from tests.definitions import SMALL_EPSILON
from tests.event_finder.event_finder_rhodesmill.definitions import ARBITRARY_ANTENNA_POSITION, ARBITRARY_FACILITY, create_expected_windows, assert_windows_eq


class TestSatellitesWithinMainBeam:
    def test_no_satellite_positions(self):
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[AntennaPosition(satellite_positions=[],
                                                                                 antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_one_satellite_position_exactly_at_antenna_position(self):
        satellite_positions = [
            ARBITRARY_ANTENNA_POSITION
        ]
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=1)
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                                 antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        expected_positions = [ARBITRARY_ANTENNA_POSITION]
        expected_windows = create_expected_windows(expected_positions)

        assert len(windows) == 1
        assert_windows_eq(windows, expected_windows)

    def test_one_satellite_position_outside_beamwidth_azimuth(self):
        satellite_positions = [
            self._replace_antenna_position(antenna_position=ARBITRARY_ANTENNA_POSITION,
                                           azimuth=ARBITRARY_ANTENNA_POSITION.position.azimuth - self._value_slightly_larger_than_half_beamwidth)
        ]
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[AntennaPosition(satellite_positions=satellite_positions,
                                                                                 antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_one_satellite_with_multiple_sequential_positions_in_view(self):
        out_of_altitude = ARBITRARY_ANTENNA_POSITION.position.altitude - self._value_slightly_larger_than_half_beamwidth
        satellite_positions = [
            self._replace_antenna_position(antenna_position=ARBITRARY_ANTENNA_POSITION,
                                           altitude=out_of_altitude if i == 2 else ARBITRARY_ANTENNA_POSITION.position.altitude,
                                           time=ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=i))
            for i in range(3)
        ]
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=len(satellite_positions))
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=satellite_positions,
                                                                  antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        expected_positions = [[satellite_positions[0], satellite_positions[1]]]
        expected_windows = create_expected_windows(expected_positions)

        assert len(windows) == 1
        assert_windows_eq(windows, expected_windows)

    def test_one_satellite_with_multiple_sequential_positions_out_of_view(self):
        out_of_altitude = ARBITRARY_ANTENNA_POSITION.position.altitude - self._value_slightly_larger_than_half_beamwidth
        satellite_positions = [
            self._replace_antenna_position(antenna_position=ARBITRARY_ANTENNA_POSITION,
                                           altitude=out_of_altitude if 0 < i < 3 else ARBITRARY_ANTENNA_POSITION.position.altitude,
                                           time=ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=i))
            for i in range(6)
        ]
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(minutes=len(satellite_positions))
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=satellite_positions,
                                                                  antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        expected_positions = [
            satellite_positions[0],
            [satellite_positions[3], satellite_positions[4], satellite_positions[5]]
        ]
        expected_windows = create_expected_windows(expected_positions)

        assert len(windows) == 2
        assert_windows_eq(windows, expected_windows)

    @property
    def _value_slightly_larger_than_half_beamwidth(self) -> float:
        return ARBITRARY_FACILITY.half_beamwidth + SMALL_EPSILON

    def test_one_satellite_below_horizon_but_within_beamwidth(self):
        antenna_position_at_horizon = self._replace_antenna_position(antenna_position=ARBITRARY_ANTENNA_POSITION,
                                                                     altitude=0)
        satellite_positions = [
            self._replace_antenna_position(antenna_position=antenna_position_at_horizon,
                                           altitude=-SMALL_EPSILON)
        ]
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=satellite_positions,
                                                                  antenna_direction=antenna_position_at_horizon)],
                                              cutoff_time=self._arbitrary_cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_no_satellites_past_cutoff_time(self):
        azimuth_outside_main_beam = ARBITRARY_ANTENNA_POSITION.position.azimuth + ARBITRARY_FACILITY.half_beamwidth + SMALL_EPSILON
        satellite_position_outside_main_beam = self._replace_antenna_position(antenna_position=ARBITRARY_ANTENNA_POSITION,
                                                                              azimuth=azimuth_outside_main_beam)
        satellite_position_inside_main_beam_but_past_cutoff_time = self._replace_antenna_position(
            antenna_position=ARBITRARY_ANTENNA_POSITION,
            time=ARBITRARY_ANTENNA_POSITION.time + timedelta(seconds=2))
        satellite_positions = [
            satellite_position_outside_main_beam,
            satellite_position_inside_main_beam_but_past_cutoff_time
        ]
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(seconds=1)
        slew = SatellitesWithinMainBeamFilter(facility=ARBITRARY_FACILITY,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=satellite_positions,
                                                                  antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        assert windows == []

    def test_satellite_reenters_horizon(self):
        facility_with_beam_width_that_sees_entire_sky = replace(ARBITRARY_FACILITY, beamwidth=360)
        satellite_positions_above_horizon = self._replace_antenna_position(ARBITRARY_ANTENNA_POSITION, altitude=1)
        satellite_positions_below_horizon = self._replace_antenna_position(ARBITRARY_ANTENNA_POSITION, altitude=-1)
        satellite_positions_without_time = [satellite_positions_above_horizon,
                                            satellite_positions_below_horizon,
                                            satellite_positions_above_horizon]
        satellite_positions = [replace(position, time=ARBITRARY_ANTENNA_POSITION.time + timedelta(seconds=i))
                               for i, position in enumerate(satellite_positions_without_time)]
        cutoff_time = ARBITRARY_ANTENNA_POSITION.time + timedelta(seconds=len(satellite_positions))
        slew = SatellitesWithinMainBeamFilter(facility=facility_with_beam_width_that_sees_entire_sky,
                                              antenna_positions=[
                                                  AntennaPosition(satellite_positions=satellite_positions,
                                                                  antenna_direction=ARBITRARY_ANTENNA_POSITION)],
                                              cutoff_time=cutoff_time)
        windows = slew.run()
        expected_positions = [satellite_positions[0], satellite_positions[2]]
        expected_windows = create_expected_windows(expected_positions)

        assert len(windows) == 2
        assert_windows_eq(windows, expected_windows)

    @property
    def _arbitrary_cutoff_time(self) -> datetime:
        return datetime.now(tz=pytz.UTC)

    @staticmethod
    def _replace_antenna_position(antenna_position: PositionTime,
                                  altitude: Optional[float] = None,
                                  azimuth: Optional[float] = None,
                                  time: Optional[datetime] = None) -> PositionTime:
        return replace(antenna_position,
                       position=replace(antenna_position.position,
                                        altitude=antenna_position.position.altitude if altitude is None else altitude,
                                        azimuth=antenna_position.position.azimuth if azimuth is None else azimuth),
                       time=antenna_position.time if time is None else time)

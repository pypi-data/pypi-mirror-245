"""Parser for Sensecap T1000 tracker.

Documentation: https://wiki.seeedstudio.com/SenseCAP_Decoder/#decoder
"""
import asyncio
import logging
import os
from datetime import datetime
from enum import Enum
from typing import Callable, Optional

import aiohttp

from ...helpers.loracloud import MGS
from ...models import LocationSources, Sensors, Uplink, WifiMacAddress

_LOGGER = logging.getLogger(__name__)


aiohttp_session: Optional[aiohttp.ClientSession] = None


class T1000:
    class Decoders:
        @staticmethod
        def battery(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            sensors.battery = data[0]
            return data[SIZE:]

        @staticmethod
        def event_mode_light(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            mode = True if data[0] else False
            setattr(sensors, "sensecap_t1000_event_mode_light", mode)
            return data[SIZE:]

        @staticmethod
        def event_mode_motion(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            mode = True if data[0] else False
            setattr(sensors, "sensecap_t1000_event_mode_motion", mode)
            return data[SIZE:]

        @staticmethod
        def event_mode_motionless(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            mode = True if data[0] else False
            setattr(sensors, "sensecap_t1000_event_mode_motionless", mode)
            return data[SIZE:]

        @staticmethod
        def event_mode_shock(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            mode = True if data[0] else False
            setattr(sensors, "sensecap_t1000_event_mode_shock", mode)
            return data[SIZE:]

        @staticmethod
        def event_mode_temperature(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            mode = True if data[0] else False
            setattr(sensors, "sensecap_t1000_event_mode_temperature", mode)
            return data[SIZE:]

        @staticmethod
        def event_status(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 3
            event_map = {
                0: "movement_start",
                1: "movement_stop",
                2: "motionless",
                3: "shock",
                4: "temperature",
                5: "light",
                6: "sos",
                7: "button",
            }
            try:
                event_str = event_map[data[2]]
            except KeyError:
                _LOGGER.warning('Unknown event status "{}"'.format(data[2]))
            else:
                setattr(sensors, "sensecap_t1000_event_status", event_str)
            return data[SIZE:]

        @staticmethod
        def gnss_coordinates(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 8
            sensors.location_source = LocationSources.GNSS
            sensors.longitude = int.from_bytes(data[:4], "big", signed=True) / 1000000
            sensors.latitude = int.from_bytes(data[4:8], "big", signed=True) / 1000000
            return data[SIZE:]

        @staticmethod
        def interval_event(sensors: Sensors, data: bytes) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False) * 60
            sensors.interval_event = interval
            return data[SIZE:]

        @staticmethod
        def interval_heartbeat(sensors: Sensors, data: bytes) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False) * 60
            sensors.interval_heartbeat = interval
            return data[SIZE:]

        @staticmethod
        def interval_motion_start(sensors: Sensors, data: bytes) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False) * 60
            setattr(sensors, "sensecap_t1000_interval_motion_start", interval)
            return data[SIZE:]

        @staticmethod
        def interval_periodic(sensors: Sensors, data: bytes) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False) * 60
            sensors.interval_periodic = interval
            return data[SIZE:]

        @staticmethod
        def interval_periodic_light_exceeded(sensors: Sensors, data: bytes) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False) * 60
            setattr(
                sensors,
                "sensecap_t1000_interval_periodic_light_exceeded",
                interval,
            )
            return data[SIZE:]

        @staticmethod
        def interval_periodic_temperature_exceeded(
            sensors: Sensors, data: bytes
        ) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False) * 60
            setattr(
                sensors,
                "sensecap_t1000_interval_periodic_temperature_exceeded",
                interval,
            )
            return data[SIZE:]

        @staticmethod
        def interval_sample_light(sensors: Sensors, data: bytes) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False)
            setattr(sensors, "sensecap_t1000_interval_sample_light", interval)
            return data[SIZE:]

        @staticmethod
        def interval_sample_temperature(sensors: Sensors, data: bytes) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False)
            setattr(sensors, "sensecap_t1000_interval_sample_temperature", interval)
            return data[SIZE:]

        @staticmethod
        def light(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            light = int.from_bytes(data[:SIZE], "big", signed=False)
            setattr(sensors, "sensecap_t1000_light_%", light)
            return data[SIZE:]

        @staticmethod
        def location_error(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 4
            error_map = {
                0x00: "GNSS timeout",
                0x01: "Wi-Fi timeout",
                0x02: "Wi-Fi+GNSS timeout",
                0x03: "GNSS+Wi-Fi timeout",
                0x04: "BLE timeout",
                0x05: "BLE+Wi-Fi timeout",
                0x06: "BLE+GNSS timeout",
                0x07: "BLE+Wi-Fi+GNSS timeout",
            }
            try:
                rule_str = error_map[data[3]]
            except KeyError:
                _LOGGER.warning('Unknown location error code "{}"'.format(data[3]))
            else:
                setattr(sensors, "sensecap_t1000_location_error", rule_str)
            return data[SIZE:]

        @staticmethod
        def location_trigger(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 3
            triggers = []
            trigger_map = {
                0x80: "button",
                0x20: "light",
                0x04: "motionless",
                0x01: "movement_start",
                0x02: "movement_stop",
                0x00: "no_event",
                0x08: "shock",
                0x40: "sos",
                0x10: "temperature",
            }
            trigger_raw = int.from_bytes(data[:SIZE], "big", signed=False) & 0xFF

            for key, value in trigger_map.items():
                if trigger_raw & key != 0:
                    triggers.append(value)

            if triggers:
                setattr(sensors, "sensecap_t1000_location_trigger", ";".join(triggers))
            else:
                setattr(sensors, "sensecap_t1000_location_trigger", trigger_map[0])

            return data[SIZE:]

        @staticmethod
        def motion_segment_number(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            segment_number = data[0]
            setattr(sensors, "sensecap_t1000_motion_segment_number", segment_number)
            return data[SIZE:]

        @staticmethod
        def positioning_status(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            status_map = {
                0: "Positioning successful",
                1: "GNSS scan timeout",
                2: "Wi-Fi scan timeout",
                3: "Wi-Fi+GNSS scan timeout",
                4: "GNSS+Wi-Fi scan timeout",
                5: "Bluetooth scan timeout",
                6: "Bluetooth+Wi-Fi scan timeout",
                7: "Bluetooth+GNSS scan timeout",
                8: "Bluetooth+Wi-Fi+GNSS scan timeout",
                9: "Location server failed to parse GNSS payload",
                10: "Location server failed to parse Wi-Fi payload",
                11: "Location server failed to parse BLE payload",
                12: "GNSS solve failed due to poor accuracy",
                13: "Time synchronization failure",
                14: "GNSS almanacs too old",
            }
            try:
                status_str = status_map[data[0]]
            except KeyError:
                _LOGGER.warning('Unknown positioning status "{}"'.format(data[0]))
            else:
                setattr(sensors, "sensecap_t1000_positioning_status", status_str)
            return data[SIZE:]

        @staticmethod
        def positioning_strategy(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            strategy_map = {
                0: "GNSS",
                1: "Wi-Fi",
                2: "Wi-Fi+GNSS",
                3: "GNSS+Wi-Fi",
                4: "Bluetooth",
                5: "Bluetooth+Wi-Fi",
                6: "Bluetooth+GNSS",
                7: "Bluetooth+Wi-Fi+GNSS",
            }
            try:
                strategy = strategy_map[data[0]]
            except KeyError:
                _LOGGER.warning('Unknown positioning strategy "{}"'.format(data[0]))
            else:
                setattr(sensors, "sensecap_t1000_positioning_strategy", strategy)
            return data[SIZE:]

        @staticmethod
        def sensors_enabled(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            state = True if data[0] else False
            setattr(sensors, "sensecap_t1000_sensors_enabled", state)
            return data[SIZE:]

        @staticmethod
        def sos_mode(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            mode_map = {
                0: "single",
                1: "continuous",
            }
            try:
                mode_str = mode_map[data[0]]
            except KeyError:
                _LOGGER.warning('Unknown SOS mode "{}"'.format(data[0]))
            else:
                setattr(sensors, "sensecap_t1000_sos_mode", mode_str)
            return data[SIZE:]

        @staticmethod
        def version_hardware(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            version = f"{data[0]}.{data[1]}"
            sensors.version_hardware = version
            return data[SIZE:]

        @staticmethod
        def version_software(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            version = f"{data[0]}.{data[1]}"
            sensors.version_software = version
            return data[SIZE:]

        @staticmethod
        def temperature(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            temperature = int.from_bytes(data[:SIZE], "big", signed=True) / 10
            sensors.temperature = temperature
            return data[SIZE:]

        @staticmethod
        def threshold_accelerometer_motion(sensors: Sensors, data: bytes) -> bytes:
            "In g"
            SIZE = 2
            threshold = int.from_bytes(data[:SIZE], "big", signed=False) / 1000
            setattr(sensors, "sensecap_t1000_threshold_accelerometer_motion", threshold)
            return data[SIZE:]

        @staticmethod
        def threshold_accelerometer_shock(sensors: Sensors, data: bytes) -> bytes:
            "In g"
            SIZE = 2
            threshold = int.from_bytes(data[:SIZE], "big", signed=False) / 1000
            setattr(sensors, "sensecap_t1000_threshold_accelerometer_shock", threshold)
            return data[SIZE:]

        @staticmethod
        def threshold_light_max(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            threshold = int.from_bytes(data[:SIZE], "big", signed=False)
            setattr(sensors, "sensecap_t1000_threshold_light_max", threshold)
            return data[SIZE:]

        @staticmethod
        def threshold_light_rule(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            rule_map = {
                0: "light ≤ min threshold",
                1: "light ≥ max threshold",
                2: "light ≤ min threshold and light ≥ max threshold",
                3: "min threshold ≤ light ≤ max threshold",
            }
            try:
                rule_str = rule_map[data[0]]
            except KeyError:
                _LOGGER.warning('Unknown light threshold rule "{}"'.format(data[0]))
            else:
                setattr(sensors, "sensecap_t1000_threshold_light_rule", rule_str)
            return data[SIZE:]

        @staticmethod
        def threshold_light_min(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            threshold = int.from_bytes(data[:SIZE], "big", signed=False)
            setattr(sensors, "sensecap_t1000_threshold_light_min", threshold)
            return data[SIZE:]

        @staticmethod
        def threshold_temperature_max(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            threshold = int.from_bytes(data[:SIZE], "big", signed=False) / 10
            setattr(sensors, "sensecap_t1000_threshold_temperature_max", threshold)
            return data[SIZE:]

        @staticmethod
        def threshold_temperature_rule(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            rule_map = {
                0: "temperature ≤ min threshold",
                1: "temperature ≥ max threshold",
                2: "temperature ≤ min threshold and temperature ≥ max threshold",
                3: "min threshold ≤ temperature ≤ max threshold",
            }
            try:
                rule_str = rule_map[data[0]]
            except KeyError:
                _LOGGER.warning(
                    'Unknown temperature threshold rule "{}"'.format(data[0])
                )
            else:
                setattr(sensors, "sensecap_t1000_threshold_temperature_rule", rule_str)
            return data[SIZE:]

        @staticmethod
        def threshold_temperature_min(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            threshold = int.from_bytes(data[:SIZE], "big", signed=False) / 10
            setattr(sensors, "sensecap_t1000_threshold_temperature_min", threshold)
            return data[SIZE:]

        @staticmethod
        def timeout_motionless(sensors: Sensors, data: bytes) -> bytes:
            """Interval in seconds"""
            SIZE = 2
            interval = int.from_bytes(data[:SIZE], "big", signed=False) * 60
            setattr(sensors, "sensecap_t1000_timeout_motionless", interval)
            return data[SIZE:]

        @staticmethod
        def timestamp(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 4
            timestamp_s = int.from_bytes(data[:SIZE], "big", signed=False)
            sensors.timestamp = datetime.utcfromtimestamp(timestamp_s)
            return data[SIZE:]

        @staticmethod
        async def wifi_mac_addresses(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 28

            mac_addresses: list[WifiMacAddress] = []
            for i in range(0, 4):
                mac_address = WifiMacAddress(
                    mac=data[i * 7 : i * 7 + 6].hex().upper(),
                    rssi=int.from_bytes(
                        data[i * 7 + 6 : i * 7 + 7], "big", signed=True
                    ),
                )
                if mac_address.mac != "FFFFFFFFFFFF":
                    mac_addresses.append(mac_address)
            sensors.location_source = LocationSources.WIFI
            setattr(sensors, "sensecap_t1000_mac_addresses", mac_addresses)

            if (
                os.environ.get("PYLIBLORAWAN_LORA_CLOUD_TOKEN", None)
                and aiohttp_session is not None
            ):
                mgs = MGS(aiohttp_session)
                location = await mgs.solve_wifi(mac_addresses)
                if location:
                    sensors.latitude = location.latitude
                    sensors.longitude = location.longitude

            return data[SIZE:]

        @staticmethod
        def working_mode(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            mode_map = {0: "standby", 1: "periodic", 2: "event"}
            try:
                mode_str = mode_map[data[0]]
            except KeyError:
                _LOGGER.warning('Unknown working mode "{}"'.format(data[0]))
            else:
                setattr(sensors, "sensecap_t1000_working_mode", mode_str)
            return data[SIZE:]

    class DataId(Enum):
        DEVICE_STATUS_EVENT = 0x01
        DEVICE_STATUS_PERIODIC = 0x02
        HEARTBEAT = 0x05
        POSITION_GNSS_SENSORS = 0x06
        POSITION_WIFI_SENSORS = 0x07
        POSITION_BLE_SENSORS = 0x08
        POSITION_GNSS_ONLY = 0x09
        POSITION_WIFI_ONLY = 0x0A
        POSITION_BLE_ONLY = 0x0B
        LOCATION_ERROR = 0x0D
        LR11xx_MIDDLEWARE_GNSS_NG_TBC = 0x0E
        ENVIRONMENTAL_SENSORS_SHORT_1 = 0x0F
        BATTERY = 0x10
        STATUS_SENSORS = 0x11

    _DECODERS: dict[DataId, list[Callable]] = {
        DataId.DEVICE_STATUS_EVENT: [
            Decoders.battery,
            Decoders.version_software,
            Decoders.version_hardware,
            Decoders.working_mode,
            Decoders.positioning_strategy,
            Decoders.interval_heartbeat,
            Decoders.interval_periodic,
            Decoders.interval_event,
            Decoders.sensors_enabled,
            Decoders.sos_mode,
            Decoders.event_mode_motion,
            Decoders.threshold_accelerometer_motion,
            Decoders.interval_motion_start,
            Decoders.event_mode_motionless,
            Decoders.timeout_motionless,
            Decoders.event_mode_shock,
            Decoders.threshold_accelerometer_shock,
            Decoders.event_mode_temperature,
            Decoders.interval_periodic_temperature_exceeded,
            Decoders.interval_sample_temperature,
            Decoders.threshold_temperature_max,
            Decoders.threshold_temperature_min,
            Decoders.threshold_temperature_rule,
            Decoders.event_mode_light,
            Decoders.interval_periodic_light_exceeded,
            Decoders.interval_sample_light,
            Decoders.threshold_light_max,
            Decoders.threshold_light_min,
            Decoders.threshold_light_rule,
        ],
        DataId.DEVICE_STATUS_PERIODIC: [
            Decoders.battery,
            Decoders.version_software,
            Decoders.version_hardware,
            Decoders.working_mode,
            Decoders.positioning_strategy,
            Decoders.interval_heartbeat,
            Decoders.interval_periodic,
            Decoders.interval_event,
            Decoders.sensors_enabled,
            Decoders.sos_mode,
        ],
        DataId.HEARTBEAT: [
            Decoders.battery,
            Decoders.working_mode,
            Decoders.positioning_strategy,
            Decoders.sos_mode,
        ],
        DataId.LOCATION_ERROR: [Decoders.location_error],
        DataId.POSITION_GNSS_ONLY: [
            Decoders.location_trigger,
            Decoders.motion_segment_number,
            Decoders.timestamp,
            Decoders.gnss_coordinates,
            Decoders.battery,
        ],
        DataId.POSITION_GNSS_SENSORS: [
            Decoders.location_trigger,
            Decoders.motion_segment_number,
            Decoders.timestamp,
            Decoders.gnss_coordinates,
            Decoders.temperature,
            Decoders.light,
            Decoders.battery,
        ],
        DataId.POSITION_WIFI_ONLY: [
            Decoders.location_trigger,
            Decoders.motion_segment_number,
            Decoders.timestamp,
            Decoders.wifi_mac_addresses,
            Decoders.battery,
        ],
        DataId.POSITION_WIFI_SENSORS: [
            Decoders.location_trigger,
            Decoders.motion_segment_number,
            Decoders.timestamp,
            Decoders.wifi_mac_addresses,
            Decoders.temperature,
            Decoders.light,
            Decoders.battery,
        ],
        DataId.STATUS_SENSORS: [
            Decoders.positioning_status,
            Decoders.event_status,
            Decoders.timestamp,
            Decoders.temperature,
            Decoders.light,
            Decoders.battery,
        ],
    }

    @staticmethod
    def _call_loracloud(sensors: Sensors, payload: bytes) -> None:
        raise NotImplementedError()

    @staticmethod
    async def _parse_payload_sensecap_t1000_5(sensors: Sensors, payload: bytes) -> None:
        """Parse payload on FPort 5."""
        try:
            data_id = T1000.DataId(payload[0])
        except ValueError:
            _LOGGER.warning('Unknown data id "{}"'.format(payload[0]))
            return

        payload = payload[1:]
        for decoder in T1000._DECODERS[data_id]:
            if asyncio.iscoroutinefunction(decoder):
                payload = await decoder(sensors, payload)
            else:
                payload = decoder(sensors, payload)

    @staticmethod
    async def parse_uplink(uplink: Uplink) -> Uplink:
        """Parse binary payload depending on FPort."""
        global aiohttp_session
        if not aiohttp_session:
            aiohttp_session = aiohttp.ClientSession(loop=asyncio.get_running_loop())

        if uplink.f_port == 5:
            await T1000._parse_payload_sensecap_t1000_5(uplink.sensors, uplink.payload)
        elif uplink.f_port >= 192 and uplink.f_port <= 199:
            T1000._call_loracloud(uplink.sensors, uplink.payload)
        else:
            _LOGGER.warning('Unknown frame port "%s"', uplink.f_port)
        return uplink

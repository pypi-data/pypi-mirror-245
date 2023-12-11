"""Parser for Tektelic Vivid sensor.

Documentation: https://support.tektelic.com/portal/en/kb/articles/srs-trm#Table_of_Technical_Reference_Manuals
"""

import logging
from enum import Enum
from typing import Callable

from ...models import Sensors, Uplink

_LOGGER = logging.getLogger(__name__)


class Vivid:
    class Decoders:
        @staticmethod
        def acceleration_magnitude(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            sensors.acceleration = int.from_bytes(data[:2], "big", signed=False) / 1000
            return data[SIZE:]

        @staticmethod
        def acceleration_vector(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 6
            sensors.acceleration_x = (
                int.from_bytes(data[0:2], "big", signed=True) / 1000
            )
            sensors.acceleration_y = (
                int.from_bytes(data[2:4], "big", signed=True) / 1000
            )
            sensors.acceleration_z = (
                int.from_bytes(data[4:6], "big", signed=True) / 1000
            )
            return data[SIZE:]

        @staticmethod
        def battery_level(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            sensors.battery_level = int.from_bytes(data[:2], "big", signed=True) / 1000
            return data[SIZE:]

        @staticmethod
        def battery_voltage(sensors: Sensors, data: bytes) -> bytes:
            """Replaced by battery_level in version 3+"""
            SIZE = 2
            sensors.battery_level = int.from_bytes(data[:2], "big", signed=True) / 100
            return data[SIZE:]

        @staticmethod
        def external_connector_analog(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            _LOGGER.warning("External connector analog value not implemented")
            return data[SIZE:]

        @staticmethod
        def external_connector_relative_count(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            _LOGGER.warning("External connector relative count not implemented")
            return data[SIZE:]

        @staticmethod
        def external_connector_state(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            input_state = False if data[0] == 0xFF else True
            setattr(sensors, "tektelic_vivid_input_state", input_state)
            return data[SIZE:]

        @staticmethod
        def external_connector_total_count(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 4
            _LOGGER.warning("External connector total count not implemented")
            return data[SIZE:]

        @staticmethod
        def humidity(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            sensors.humidity = data[0] / 2
            return data[SIZE:]

        @staticmethod
        def light_detected(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            sensors.light_detected = True if data[0] == 0xFF else False
            return data[SIZE:]

        @staticmethod
        def light_intensity(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            _LOGGER.warning("Uncalibrated light intensity not implemented")
            return data[SIZE:]

        @staticmethod
        def impact_detected(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            impact = True if data[0] == 0xFF else False
            setattr(sensors, "tektelic_vivid_impact_detected", impact)
            return data[SIZE:]

        @staticmethod
        def magnet_detected(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            sensors.magnet_detected = True if data[0] == 0x00 else False
            return data[SIZE:]

        @staticmethod
        def motion_detected(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 1
            sensors.motion_detected = True if data[0] == 0xFF else False
            return data[SIZE:]

        @staticmethod
        def mcu_temperature(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            _LOGGER.warning("MCU temperature not implemented")
            return data[SIZE:]

        @staticmethod
        def temperature(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            sensors.temperature = int.from_bytes(data[:2], "big", signed=True) / 10
            return data[SIZE:]

        @staticmethod
        def total_event_counter(sensors: Sensors, data: bytes) -> bytes:
            SIZE = 2
            sensors.total_event_counter = data[0]
            return data[SIZE:]

    class ChannelTypeId(Enum):
        ACCELERATION_MAGNITUDE = 0x0502
        ACCELERATION_VECTOR = 0x0771
        BATTERY_LEVEL = 0x00BA
        BATTERY_VOLTAGE = 0x00FF
        EXTERNAL_CONNECTOR_ANALOG = 0x1102
        EXTERNAL_CONNECTOR_RELATIVE_COUNT = 0x0F04
        EXTERNAL_CONNECTOR_STATE = 0x0E00
        EXTERNAL_CONNECTOR_TOTAL_COUNT = 0x1204
        HUMIDITY = 0x0468
        IMPACT_DETECTED = 0x0C00
        LIGHT_DETECTED = 0x0200
        LIGHT_INTENSITY = 0x1002
        MAGNET_DETECTED = 0x0100
        MAGNET_DETECTED_COUNTER = 0x0804
        MCU_TEMPERATURE = 0x0B67
        MOTION_DETECTED = 0x0A00
        MOTION_DETECTED_COUNTER = 0x0D04
        TEMPERATURE = 0x0367

    _DECODERS: dict[ChannelTypeId, Callable] = {
        ChannelTypeId.ACCELERATION_MAGNITUDE: Decoders.acceleration_magnitude,
        ChannelTypeId.ACCELERATION_VECTOR: Decoders.acceleration_vector,
        ChannelTypeId.BATTERY_LEVEL: Decoders.battery_level,
        ChannelTypeId.BATTERY_VOLTAGE: Decoders.battery_voltage,
        ChannelTypeId.EXTERNAL_CONNECTOR_ANALOG: Decoders.external_connector_analog,
        ChannelTypeId.EXTERNAL_CONNECTOR_RELATIVE_COUNT: Decoders.external_connector_relative_count,
        ChannelTypeId.EXTERNAL_CONNECTOR_STATE: Decoders.external_connector_state,
        ChannelTypeId.EXTERNAL_CONNECTOR_TOTAL_COUNT: Decoders.external_connector_total_count,
        ChannelTypeId.HUMIDITY: Decoders.humidity,
        ChannelTypeId.IMPACT_DETECTED: Decoders.impact_detected,
        ChannelTypeId.LIGHT_DETECTED: Decoders.light_detected,
        ChannelTypeId.LIGHT_INTENSITY: Decoders.light_intensity,
        ChannelTypeId.MAGNET_DETECTED: Decoders.magnet_detected,
        ChannelTypeId.MAGNET_DETECTED_COUNTER: Decoders.total_event_counter,
        ChannelTypeId.MCU_TEMPERATURE: Decoders.mcu_temperature,
        ChannelTypeId.MOTION_DETECTED: Decoders.motion_detected,
        ChannelTypeId.MOTION_DETECTED_COUNTER: Decoders.total_event_counter,
        ChannelTypeId.TEMPERATURE: Decoders.temperature,
    }

    @staticmethod
    def _parse_port_5(sensors: Sensors, payload: bytes) -> None:
        """Parse payload on FPort 5."""
        _LOGGER.warning("System diagnostics parsing not implemented")

    @staticmethod
    def _parse_port_10(sensors: Sensors, payload: bytes) -> None:
        """Parse payload on FPort 10."""

        while payload:
            try:
                channel_type_id = Vivid.ChannelTypeId(
                    int.from_bytes(payload[:2], "big")
                )
            except ValueError:
                _LOGGER.error(
                    'Unknown data channel and type id "{}"'.format(payload[:2].hex())
                )
                return

            payload = payload[2:]
            decoder = Vivid._DECODERS[channel_type_id]
            payload = decoder(sensors, payload)

    @staticmethod
    async def parse_uplink(uplink: Uplink) -> Uplink:
        """Parse binary payload depending on FPort."""
        if uplink.f_port == 5:
            Vivid._parse_port_5(uplink.sensors, uplink.payload)
        elif uplink.f_port == 10:
            Vivid._parse_port_10(uplink.sensors, uplink.payload)
        else:
            _LOGGER.warning('Unknown frame port "%s"', uplink.f_port)
        return uplink

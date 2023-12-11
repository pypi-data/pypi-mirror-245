"""Parser for Elsys ERS Eco temperature/humidity sensor.

Documentation: https://elsys.se/public/app_notes/AppNote_ELSYS_uplink_payload.pdf
"""
import logging
from dataclasses import dataclass
from enum import Enum

from ...models import Sensors, Uplink

_LOGGER = logging.getLogger(__name__)


class DataTypes(Enum):
    TEMPERATURE = 1
    HUMIDITY = 2
    LIGHT = 4
    BATTERY = 7


@dataclass
class TypeDetail:
    name: str
    size: int
    scale: float = 1
    signed: bool = False


types = {
    DataTypes.BATTERY.value: TypeDetail(name="battery_level", scale=0.001, size=2),
    DataTypes.HUMIDITY.value: TypeDetail(name="humidity", size=1),
    DataTypes.LIGHT.value: TypeDetail(name="illuminance", size=2),
    DataTypes.TEMPERATURE.value: TypeDetail(
        name="temperature", scale=0.1, signed=True, size=2
    ),
}


class ErsEco:
    @staticmethod
    def _parse_payload_erseco_5(sensors: Sensors, payload: bytes) -> None:
        """Parse payload on FPort 5."""

        while len(payload) > 0:
            try:
                decoder = types[payload[0] & 0x3F]
            except KeyError:
                _LOGGER.error(f'Unable to parse type "{payload[0] & 0x3F}"')
                return
            data_raw = payload[1 : 1 + decoder.size]
            data = round(
                int.from_bytes(data_raw, "big", signed=decoder.signed) * decoder.scale,
                2,
            )
            setattr(sensors, decoder.name, data)
            payload = payload[1 + decoder.size :]

    @staticmethod
    async def parse_uplink(uplink: Uplink) -> Uplink:
        """Parse binary payload depending on FPort."""
        if uplink.f_port == 5:
            ErsEco._parse_payload_erseco_5(uplink.sensors, uplink.payload)
        else:
            _LOGGER.warning('Unknown frame port "%s"', uplink.f_port)

        return uplink

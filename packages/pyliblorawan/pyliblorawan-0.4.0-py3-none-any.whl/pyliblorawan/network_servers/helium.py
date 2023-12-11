"""Parser for Helium network server."""
import base64
import logging

import aiohttp

from ..helpers.exceptions import CannotConnect, InvalidAuth
from ..models import Device, NetworkServer, Uplink

_LOGGER = logging.getLogger(__name__)


USER_AGENT = "pyLibLoRaWAN"


class Helium(NetworkServer):
    """Network server class for Helium."""

    def __init__(self, api_key: str, url: str) -> None:
        """Construct the Helium object.

        :param api_key: Helium API Key
        :param url: Helium URL
        """
        self._url = url
        self._headers = {
            "Accept": "application/json",
            "Key": api_key,
            "User-Agent": USER_AGENT,
        }

        if self._url[-1] != "/":
            self._url += "/"

    @staticmethod
    def is_compatible_uplink(uplink: dict) -> bool:
        """Return True if the payload is compatible with this NS"""
        try:
            uplink["hotspots"]
            uplink["reported_at"]
            return True
        except KeyError:
            return False

    async def list_devices(self, session: aiohttp.ClientSession) -> list[Device]:
        """List device euis of the organization"""
        async with session.request(
            "GET",
            f"{self._url}api/v1/devices",
            headers=self._headers,
        ) as res:
            if res.status == 401:
                raise InvalidAuth
            if res.status < 200 or res.status >= 300:
                raise CannotConnect(res.status)
            devices = await res.json()
            return [
                Device(device_eui=device["dev_eui"], name=device["name"])
                for device in devices
            ]

    @staticmethod
    def normalize_uplink(uplink: dict) -> Uplink:
        """Parse Helium uplink json to internal object model"""
        return Uplink(
            device_eui=uplink["dev_eui"],
            payload=base64.b64decode(uplink["payload"]),
            f_port=uplink["port"],
        )

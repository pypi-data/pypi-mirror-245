"""Parser for The Things Network (V3) network server."""
import base64
import logging

import aiohttp

from ..helpers.exceptions import CannotConnect, InvalidAuth
from ..models import Device, NetworkServer, Uplink

_LOGGER = logging.getLogger(__name__)

USER_AGENT = "pyLibLoRaWAN"


class TTN(NetworkServer):
    """Network server class for TTN."""

    def __init__(self, api_key: str, application: str, url: str) -> None:
        """Construct the TTN object.

        :param api_key: TTN application API Key (rights: View devices in application, Read application traffic, Write downlink application traffic)"
        :param application: TTN application ID
        :param url: TTN URL
        """
        self._application = application
        self._url = url
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }

        if self._url[-1] != "/":
            self._url += "/"

    @staticmethod
    def is_compatible_uplink(uplink: dict) -> bool:
        """Return True if the payload is compatible with this NS"""
        try:
            uplink["end_device_ids"]
            uplink["uplink_message"]
            return True
        except KeyError:
            return False

    async def list_devices(self, session: aiohttp.ClientSession) -> list[Device]:
        """List device euis of the TTN application"""
        async with session.request(
            "GET",
            f"{self._url}api/v3/applications/{self._application}/devices",
            headers=self._headers,
        ) as res:
            if res.status == 401:
                raise InvalidAuth
            if res.status < 200 or res.status >= 300:
                raise CannotConnect(res.status)
            devices = (await res.json())["end_devices"]
            # TODO: Handle pages
            return [
                Device(device["ids"]["dev_eui"], device["ids"]["device_id"])
                for device in devices
            ]

    @staticmethod
    def normalize_uplink(uplink: dict) -> Uplink:
        """Parse TTN uplink json to internal object model"""
        return Uplink(
            device_eui=uplink["end_device_ids"]["dev_eui"].upper(),
            payload=base64.b64decode(uplink["uplink_message"]["frm_payload"]),
            f_port=uplink["uplink_message"]["f_port"],
        )

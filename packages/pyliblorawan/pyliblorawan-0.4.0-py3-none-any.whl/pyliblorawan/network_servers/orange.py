"""Parser for Orange network server."""
import logging

import aiohttp

from ..helpers.exceptions import CannotConnect, InvalidAuth
from ..models import Device, NetworkServer, Uplink

_LOGGER = logging.getLogger(__name__)


USER_AGENT = "pyLibLoRaWAN"


class Orange(NetworkServer):
    """Network server class for Orange."""

    def __init__(self, api_key: str) -> None:
        """Construct the Orange object.

        :param api_key: Orange API Key
        """
        self._url = "https://liveobjects.orange-business.com/"
        self._headers = {
            "Accept": "application/json",
            "X-API-KEY": api_key,
            "User-Agent": USER_AGENT,
        }

    @staticmethod
    def is_compatible_uplink(uplink: dict) -> bool:
        """Return True if the payload is compatible with this NS"""
        try:
            uplink["streamId"]
            uplink["created"]
            return True
        except KeyError:
            return False

    async def list_device_euis(self, session: aiohttp.ClientSession) -> list[Device]:
        """List device euis of the organization"""
        devices: list[Device] = []
        last_id = ""
        while True:
            try:
                async with session.request(
                    "GET",
                    f"{self._url}api/v1/deviceMgt/devices?limit=50&bookmarkId={last_id}",
                    headers=self._headers,
                ) as res:
                    if res.status == 401:
                        raise InvalidAuth
                    if res.status < 200 or res.status >= 300:
                        raise CannotConnect(res.status)

                    for device in await res.json():
                        device_eui = device["id"].split(":")[-1]
                        name = device.get("name", device_eui)
                        devices.append(Device(device_eui=device_eui, name=name))
                        last_id = device["id"]

                    if res.headers["X-Result-Limit"] != res.headers["X-Result-Count"]:
                        break
            except aiohttp.ClientConnectionError:
                # When API key is invalid Orange does not allow connection
                raise InvalidAuth()
        return devices

    @staticmethod
    def normalize_uplink(uplink: dict) -> Uplink:
        """Parse Orange uplink json to internal object model"""
        return Uplink(
            device_eui=uplink["metadata"]["network"]["lora"]["devEUI"],
            payload=bytes.fromhex(uplink["value"]["payload"]),
            f_port=uplink["metadata"]["network"]["lora"]["port"],
        )

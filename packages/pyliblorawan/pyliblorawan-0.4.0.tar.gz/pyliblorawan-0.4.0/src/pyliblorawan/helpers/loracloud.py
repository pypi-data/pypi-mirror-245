import json
import os
from typing import Optional

import aiohttp

from ..helpers.exceptions import CannotConnect, InvalidAuth
from ..models import Location, LocationSources, WifiMacAddress


class MGS:
    def __init__(self, session: aiohttp.ClientSession):
        self._lora_cloud_server = os.environ.get(
            "PYLIBLORAWAN_LORA_CLOUD_SERVER", "mgs.loracloud.com"
        )
        self._headers = {
            "accept": "application/json",
            "authorization": os.environ["PYLIBLORAWAN_LORA_CLOUD_TOKEN"],
            "content-type": "application/json",
        }
        self._session = session

    async def solve_wifi(
        self, mac_addresses: list[WifiMacAddress]
    ) -> Optional[Location]:
        data: dict[str, list[dict]] = {
            "lorawan": [
                {
                    "gatewayId": "fake-gateway",
                    "rssi": 0,
                    "snr": 0,
                    "toa": 0,
                    "antennaId": 0,
                    "antennaLocation": {
                        "latitude": 46.983753,
                        "longitude": 6.906008,
                        "altitude": 479,
                    },
                }
            ],
            "wifiAccessPoints": [],
        }
        for mac_address in mac_addresses:
            data["wifiAccessPoints"].append(
                {"macAddress": mac_address.mac, "signalStrength": mac_address.rssi}
            )

        async with self._session.post(
            url=f"https://{self._lora_cloud_server}/api/v1/solve/loraWifi",
            headers=self._headers,
            data=json.dumps(data),
        ) as res:
            if res.status == 401:
                raise InvalidAuth
            if res.status < 200 or res.status >= 300:
                raise CannotConnect(res.status)
            data_mgs = await res.json()

            if data_mgs.get("result", None) == None:
                return None

            return Location(
                latitude=data_mgs["result"]["latitude"],
                longitude=data_mgs["result"]["longitude"],
                source=LocationSources.WIFI,
                accuracy=data_mgs["result"]["accuracy"],
            )

import json

import aiohttp
import pytest
from aioresponses import CallbackResult, aioresponses

from pyliblorawan.helpers.exceptions import CannotConnect, InvalidAuth
from pyliblorawan.models import Device
from pyliblorawan.network_servers.helium import Helium


def callback_get_devices(url: str, **kwargs) -> CallbackResult:
    assert kwargs["headers"]["Key"] == "TEST-API-KEY"
    assert kwargs["headers"]["Accept"] == "application/json"
    assert kwargs["headers"]["User-Agent"] == "pyLibLoRaWAN"

    return CallbackResult(
        body=json.dumps(
            [
                {
                    "active": True,
                    "adr_allowed": None,
                    "app_eui": "00112233445566AA",
                    "app_key": "00000000000000000000000000000011",
                    "app_s_key": "00000000000000000000000000000022",
                    "cf_list_enabled": None,
                    "config_profile_id": None,
                    "dc_usage": 126904,
                    "dev_eui": "00112233445566BB",
                    "devaddr": "480008C8",
                    "id": "9585ef67-51a4-4320-96a7-0d969f22f2e3",
                    "in_xor_filter": True,
                    "labels": [
                        {
                            "adr_allowed": False,
                            "cf_list_enabled": True,
                            "config_profile_id": "bea2b1ef-f013-4709-80b2-df88d15d54b1",
                            "id": "acv56f48-0f'1-4a1b-8e47-0e30b84875ac",
                            "name": "TEST-LABEL",
                            "rx_delay": 5,
                        }
                    ],
                    "last_connected": "2023-01-10T16:28:03",
                    "name": "TEST-DEVICE",
                    "nwk_s_key": "00000000000000000000000000000033",
                    "organization_id": "d724293a-89ca-4075-98e2-872bce31050b",
                    "oui": 24,
                    "region": "AU915",
                    "rx_delay": 1,
                    "total_packets": 124036,
                }
            ]
        )
    )


def test_constructor():
    ns = Helium(api_key="TEST-API-KEY", url="http://TEST.URL")

    assert ns._url == "http://TEST.URL/"
    assert ns._headers == {
        "Accept": "application/json",
        "Key": "TEST-API-KEY",
        "User-Agent": "pyLibLoRaWAN",
    }

    # Test that '/' is not added if existing
    ns = Helium("TEST-API-KEY", "http://TEST.URL/")
    assert ns._url == "http://TEST.URL/"


def test_normalize_uplink(helium_uplink: dict):
    ns = Helium("TEST-API-KEY", "http://TEST.URL")
    uplink = ns.normalize_uplink(helium_uplink)

    assert uplink.device_eui == "00112233445566BB"
    assert uplink.f_port == 123
    assert uplink.payload == bytes.fromhex("FE00ED")


def test_is_compatible_uplink():
    assert Helium.is_compatible_uplink({}) == False
    assert Helium.is_compatible_uplink({"hotspots": None}) == False
    assert Helium.is_compatible_uplink({"reported_at": None}) == False
    assert Helium.is_compatible_uplink({"hotspots": None, "reported_at": None}) == True


@pytest.mark.asyncio
async def test_list_devices():
    ns = Helium("TEST-API-KEY", "http://TEST.URL")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "http://TEST.URL/api/v1/devices",
            callback=callback_get_devices,
        )
        devices = await ns.list_devices(session)
        assert devices == [Device("00112233445566BB", "TEST-DEVICE")]

    await session.close()


@pytest.mark.asyncio
async def test_list_devices_unauthorized():
    ns = Helium("TEST-API-KEY", "http://TEST.URL")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "http://TEST.URL/api/v1/devices",
            status=401,
        )
        with pytest.raises(InvalidAuth):
            _ = await ns.list_devices(session)

    await session.close()


@pytest.mark.asyncio
async def test_list_devices_unknown():
    ns = Helium("TEST-API-KEY", "http://TEST.URL")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "http://TEST.URL/api/v1/devices",
            status=400,
        )
        with pytest.raises(CannotConnect) as e:
            _ = await ns.list_devices(session)
        assert str(e.value) == "400"

    await session.close()

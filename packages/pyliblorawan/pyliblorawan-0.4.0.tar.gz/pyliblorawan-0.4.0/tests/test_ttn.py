import aiohttp
import pytest
from aioresponses import CallbackResult, aioresponses

from pyliblorawan.helpers.exceptions import CannotConnect, InvalidAuth
from pyliblorawan.models import Device
from pyliblorawan.network_servers.ttn import TTN


def callback_get_devices(url: str, **kwargs) -> CallbackResult:
    assert kwargs["headers"]["Authorization"] == "Bearer TEST-API-KEY"
    assert kwargs["headers"]["Accept"] == "application/json"
    assert kwargs["headers"]["User-Agent"] == "pyLibLoRaWAN"

    return CallbackResult(
        payload={
            "end_devices": [
                {
                    "ids": {
                        "device_id": "TEST-DEVICE",
                        "application_ids": {"application_id": "TEST-APPLICATION"},
                        "dev_eui": "FEEDABCD00000002",
                        "join_eui": "FEEDABCD00000001",
                    },
                    "created_at": "2023-07-24T23:35:49.598651Z",
                    "updated_at": "2023-07-24T23:35:49.598651Z",
                }
            ]
        }
    )


def test_constructor():
    ns = TTN("TEST-API-KEY", "TEST-APPLICATION", "http://TEST.URL")

    assert ns._application == "TEST-APPLICATION"
    assert ns._url == "http://TEST.URL/"
    assert ns._headers == {
        "Accept": "application/json",
        "Authorization": "Bearer TEST-API-KEY",
        "User-Agent": "pyLibLoRaWAN",
    }

    # Test that '/' is not added if existing
    ns = TTN("TEST-API-KEY", "TEST-APPLICATION", "http://TEST.URL/")
    assert ns._url == "http://TEST.URL/"


def test_normalize_uplink(ttn_uplink):
    ns = TTN("TEST-API-KEY", "TEST-APPLICATION", "http://TEST.URL")
    uplink = ns.normalize_uplink(ttn_uplink)

    assert uplink.device_eui == "FEEDABCD00000002"
    assert uplink.f_port == 123
    assert uplink.payload == bytes.fromhex("FE00ED")


def test_is_compatible_uplink():
    assert TTN.is_compatible_uplink({}) == False
    assert TTN.is_compatible_uplink({"end_device_ids": None}) == False
    assert TTN.is_compatible_uplink({"uplink_message": None}) == False
    assert (
        TTN.is_compatible_uplink({"end_device_ids": None, "uplink_message": None})
        == True
    )


@pytest.mark.asyncio
async def test_list_devices():
    ns = TTN("TEST-API-KEY", "TEST-APPLICATION", "http://TEST.URL")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "http://TEST.URL/api/v3/applications/TEST-APPLICATION/devices",
            callback=callback_get_devices,
        )
        devices = await ns.list_devices(session)
        assert devices == [Device("FEEDABCD00000002", "TEST-DEVICE")]

    await session.close()


@pytest.mark.asyncio
async def test_list_devices_unauthorized():
    ns = TTN("TEST-API-KEY", "TEST-APPLICATION", "http://TEST.URL")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "http://TEST.URL/api/v3/applications/TEST-APPLICATION/devices",
            status=401,
        )
        with pytest.raises(InvalidAuth):
            _ = await ns.list_devices(session)

    await session.close()


@pytest.mark.asyncio
async def test_list_devices_unknown():
    ns = TTN("TEST-API-KEY", "TEST-APPLICATION", "http://TEST.URL")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "http://TEST.URL/api/v3/applications/TEST-APPLICATION/devices",
            status=400,
        )
        with pytest.raises(CannotConnect) as e:
            _ = await ns.list_devices(session)
        assert str(e.value) == "400"

    await session.close()

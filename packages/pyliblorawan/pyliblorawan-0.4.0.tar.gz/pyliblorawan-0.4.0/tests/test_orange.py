import json

import aiohttp
import pytest
import yarl
from aioresponses import CallbackResult, aioresponses

from pyliblorawan.helpers.exceptions import CannotConnect, InvalidAuth
from pyliblorawan.models import Device
from pyliblorawan.network_servers.orange import Orange


def callback_get_devices(url: yarl.URL, **kwargs) -> CallbackResult:
    assert kwargs["headers"]["X-API-KEY"] == "TEST-API-KEY"
    assert kwargs["headers"]["Accept"] == "application/json"
    assert kwargs["headers"]["User-Agent"] == "pyLibLoRaWAN"

    if url.query.get("bookmarkId"):
        assert url.query["bookmarkId"] == "urn%3Alo%3Ansid%3Alora%3A00112233445566DD"
        headers = {
            "X-Result-Limit": "2",
            "X-Result-Count": "1",
        }
        body = [
            {
                "id": "urn:lo:nsid:lora:00112233445566EE",
                "name": "TEST-DEVICE-5566EE",
                "tags": [""],
                "group": {"id": "s3m9YP", "path": "/"},
            }
        ]

    else:
        headers = {
            "X-Result-Limit": "2",
            "X-Result-Count": "2",
        }
        body = [
            {
                "id": "urn:lo:nsid:lora:00112233445566CC",
                "name": "TEST-DEVICE-5566CC",
                "tags": [""],
                "group": {"id": "s3m9YP", "path": "/"},
            },
            {
                "id": "urn:lo:nsid:lora:00112233445566DD",
                "name": "TEST-DEVICE-5566DD",
                "tags": [""],
                "group": {"id": "s3m9YP", "path": "/"},
            },
        ]

    return CallbackResult(headers=headers, body=json.dumps(body))


def test_constructor():
    ns = Orange(api_key="TEST-API-KEY")

    assert ns._url == "https://liveobjects.orange-business.com/"
    assert ns._headers == {
        "Accept": "application/json",
        "X-API-KEY": "TEST-API-KEY",
        "User-Agent": "pyLibLoRaWAN",
    }


def test_normalize_uplink(orange_uplink: dict):
    ns = Orange(api_key="TEST-API-KEY")
    uplink = ns.normalize_uplink(orange_uplink)

    assert uplink.device_eui == "00112233445566CC"
    assert uplink.f_port == 123
    assert uplink.payload == bytes.fromhex("FE00ED")


def test_is_compatible_uplink():
    assert Orange.is_compatible_uplink({}) == False
    assert Orange.is_compatible_uplink({"streamId": None}) == False
    assert Orange.is_compatible_uplink({"created": None}) == False
    assert Orange.is_compatible_uplink({"streamId": None, "created": None}) == True


@pytest.mark.asyncio
async def test_list_device_euis():
    ns = Orange(api_key="TEST-API-KEY")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "https://liveobjects.orange-business.com/api/v1/deviceMgt/devices?limit=50&bookmarkId=",
            callback=callback_get_devices,
        )
        m.get(
            "https://liveobjects.orange-business.com/api/v1/deviceMgt/devices?limit=50&bookmarkId=urn:lo:nsid:lora:00112233445566DD",
            callback=callback_get_devices,
        )
        devices = await ns.list_device_euis(session)
        assert devices == [
            Device("00112233445566CC", "TEST-DEVICE-5566CC"),
            Device("00112233445566DD", "TEST-DEVICE-5566DD"),
            Device("00112233445566EE", "TEST-DEVICE-5566EE"),
        ]

    await session.close()


@pytest.mark.asyncio
async def test_list_device_euis_unauthorized():
    ns = Orange(api_key="TEST-API-KEY")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "https://liveobjects.orange-business.com/api/v1/deviceMgt/devices?limit=50&bookmarkId=",
            status=401,
        )
        with pytest.raises(InvalidAuth):
            _ = await ns.list_device_euis(session)

    await session.close()


@pytest.mark.asyncio
async def test_list_device_euis_incorrect():
    ns = Orange(api_key="TEST-API-KEY")
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "https://liveobjects.orange-business.com/api/v1/deviceMgt/devices?limit=50&bookmarkId=",
            status=400,
        )
        with pytest.raises(CannotConnect):
            _ = await ns.list_device_euis(session)

    await session.close()


@pytest.mark.asyncio
async def test_list_device_euis_wrong_api_key():
    ns = Orange(api_key="TEST-API-KEY")
    ns._url = "http://"
    session = aiohttp.ClientSession()

    with aioresponses() as m:
        m.get(
            "https://liveobjects.orange-business.com/api/v1/deviceMgt/devices?limit=50&bookmarkId=",
            status=400,
        )
        with pytest.raises(InvalidAuth):
            _ = await ns.list_device_euis(session)

    await session.close()

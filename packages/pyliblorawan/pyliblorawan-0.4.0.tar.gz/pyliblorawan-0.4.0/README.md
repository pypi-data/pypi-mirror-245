# pyLibLoRaWAN - Python library to interface with LoRaWAN devices and network servers

## Introduction

This library aims to enable LoRaWAN the [Home Assistant](https://www.home-assistant.io/) integration to interact with LoRaWAN network servers and devices, but can be reused for other purposes.

## Compatibility list

### Network servers

- [Helium](https://www.helium.com/), either from the [the foundation](https://console.helium.com/) or self hosted
- [Orange Live Objects](https://liveobjects.orange-business.com/), a French operator
- [The Things Stack](https://www.thethingsindustries.com/docs/getting-started/the-things-stack-basics/): [TTN](https://www.thethingsnetwork.org/), [TTI](https://www.thethingsindustries.com/) or self hosted

### Devices

- [Browan TBMS100](https://www.browan.com/product/motion-sensor-pir/detail): PIR motion sensor

## Usage

### Usage - Network servers

Import the network server object then call the input normalization formatter function:

```Python
from pyliblorawan.network_servers.ttn import TTN

ns = TTN(**kwargs)
uplink = ns.normalize_uplink(ttn_uplink_dict)
```

Some other functions are available:

- `list_devices`: List devices in the authorized scope

### Usage - Devices

Import the device object then call the payload parser function:

```Python
from pyliblorawan.devices.browan.tbms100 import TBMS100

device = TBMS100()
await tbms100.parse_uplink(uplink_object)
```

## Test

Install `requirements.txt` and `requirements-dev.txt` then:

```bash
python3 -m pytest -vv --cov=. --cov-config=tests/.coveragerc tests/
```

"""Exception set for Python LoRaWAN library."""


class PyLibLorawanError(Exception):
    """Generic error class for the libray"""


class CannotConnect(PyLibLorawanError):
    """Any HTTP issue excep 401-Unauthorized."""


class DeviceEuiNotFound(PyLibLorawanError):
    """When the device is not found in the network server."""


class InvalidAuth(PyLibLorawanError):
    """When authentication credentials are refused"""


class InvalidDeviceEui(PyLibLorawanError):
    """Error to indicate a malformed device EUI."""

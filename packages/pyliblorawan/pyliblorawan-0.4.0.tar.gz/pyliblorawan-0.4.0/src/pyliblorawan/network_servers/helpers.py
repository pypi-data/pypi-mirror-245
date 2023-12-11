import logging

from ..models import Uplink
from .helium import Helium
from .orange import Orange
from .ttn import TTN

_LOGGER = logging.getLogger(__name__)


def normalize_unknown_uplink(uplink: dict) -> Uplink:
    """Parse an uplink json to internal object model when ns is known"""
    if Helium.is_compatible_uplink(uplink):
        return Helium.normalize_uplink(uplink)
    elif Orange.is_compatible_uplink(uplink):
        return Orange.normalize_uplink(uplink)
    elif TTN.is_compatible_uplink(uplink):
        return TTN.normalize_uplink(uplink)
    else:
        _LOGGER.error("Unable to parse uplink, unknown NS")
        _LOGGER.error("{}".format(uplink))
        raise ValueError("Unable to parse uplink, unknown NS")

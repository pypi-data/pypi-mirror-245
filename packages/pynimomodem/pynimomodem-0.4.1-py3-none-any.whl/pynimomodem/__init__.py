"""Library to interface with a Viasat-approved NIMO modem for satellite IoT.

Depends on either Python/PySerial or Micropython/machine library.

"""

from .constants import (
    AtErrorCode,
    BeamState,
    ControlState,
    EventNotification,
    GnssMode,
    MessagePriority,
    MessageState,
    NetworkStatus,
    PowerMode,
    SignalQuality,
    UrcCode,
    UrcControl,
    WakeupPeriod,
    WakeupWay,
    WorkMode,
)
from .modem import (
    Manufacturer,
    ModemLocation,
    MoMessage,
    MtMessage,
    NimoModem,
    ModemError,
    SatelliteAcquisitionDetail,
    SatelliteLocation,
)

__all__ = [
    'AtErrorCode',
    'BeamState',
    'ControlState',
    'GnssMode',
    'Manufacturer',
    'MessagePriority',
    'MessageState',
    'ModemLocation',
    'MoMessage',
    'MtMessage',
    'NetworkStatus',
    'NimoModem',
    'ModemError',
    'PowerMode',
    'SatelliteAcquisitionDetail',
    'SatelliteLocation',
    'SignalQuality',
    'WakeupPeriod',
    'WakeupWay',
    'WorkMode',
    'UrcCode',
    'UrcControl',
    'EventNotification',
]
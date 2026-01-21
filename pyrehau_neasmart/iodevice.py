import time
from .utils import autoupdate_property

class RehauNeaSmartIoDevice(object):
    def __init__(self, bridge, id, auto_update=True):
        self._id = id
        self._bridge = bridge
        self._last_refresh_time = 0
        self._auto_update = auto_update

    def _make_request(self, type='GET', request=None):
        return self._bridge._make_request(type=type, request=request)

    def _update_if_needed(self):
        """Check whether the existing status is too stale and update it if so."""
        if self._auto_update and time.time() - self._last_refresh_time >= 1:
            self._update_status()

    def _update_status(self):
        """Fetch the device's current status from the bridge."""
        status_line = self._make_request()

        for child in status_line.iter(tag='IODEVICE'):
            if child.attrib['nr'] == self._id:
                for subelem in child:
                    setattr(self, '_' + subelem.tag.lower(), subelem.text)

        self._last_refresh_time = time.time()

    def _clear_status(self):
        """Force the next property read to refresh the device status."""
        self._last_refresh_time = 0

    def update_status(self):
        """Force a status update."""
        self._clear_status()
        self._update_status()

    @autoupdate_property
    def status(self):
        return {
            "iodevice_type": self._iodevice_type,
            "iodevice_id": self._iodevice_id,
            "iodevice_vers_hw": self._iodevice_vers_hw,
            "iodevice_vers_sw": self._iodevice_vers_sw,
            "heatarea_nr": self._heatarea_nr,
            "signalstrength": self._signalstrength,
            "battery": self._battery,
            "iodevice_state": self._iodevice_state,
            "iodevice_comerror": self._iodevice_comerror,
            "ison": self._ison
        }

    @autoupdate_property
    def iodevice_type(self):
        return self._iodevice_type

    @autoupdate_property
    def iodevice_id(self):
        return self._iodevice_id

    @autoupdate_property
    def iodevice_vers_hw(self):
        return self._iodevice_vers_hw

    @autoupdate_property
    def iodevice_vers_sw(self):
        return self._iodevice_vers_sw

    @autoupdate_property
    def heatarea_nr(self):
        return self._heatarea_nr

    @autoupdate_property
    def signalstrength(self):
        return self._signalstrength

    @autoupdate_property
    def battery(self):
        return self._battery

    @autoupdate_property
    def iodevice_state(self):
        return self._iodevice_state

    @autoupdate_property
    def iodevice_comerror(self):
        return self._iodevice_comerror

    @autoupdate_property
    def ison(self):
        return self._ison

    @property
    def id(self):
        return self._id

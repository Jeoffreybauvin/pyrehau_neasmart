import time
from .utils import autoupdate_property

class RehauNeaSmartDevice(object):
    def __init__(self, bridge, auto_update=True):
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

        # The root is <Devices> and first child is <Device>
        # We look for the first Device tag
        for child in status_line.iter(tag='Device'):
            for subelem in child:
                # We skip complex types or handle them if requested?
                # User asked for specific fields which are direct children of Device
                # But Vacation, Network, Cloud, Code, Program, etc are also children.
                # Assuming flattened strings for now or just the requested ones.
                # The requested list are all simple text nodes except maybe keys like MASTERID if it exists.
                if len(list(subelem)) == 0:
                    setattr(self, '_' + subelem.tag.lower(), subelem.text)
            
            # We only start with the first device found as per request implied single device info
            break

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
            "id": self._id,
            "type": self._type,
            "name": self._name,
            "origin": self._origin,
            "errorcount": self._errorcount,
            "datetime": self._datetime,
            "dayofweek": self._dayofweek,
            "timezone": self._timezone,
            "ntptimesync": self._ntptimesync,
            "vers_sw_stm": self._vers_sw_stm,
            "vers_sw_eth": self._vers_sw_eth,
            "vers_hw": self._vers_hw,
            "temperatureunit": self._temperatureunit,
            "summerwinter": self._summerwinter,
            "tps": self._tps,
            "limiter": self._limiter,
            "masterid": self._masterid,
            "changeover": self._changeover,
            "cooling": self._cooling,
            "mode": self._mode,
            "operationmode_actor": self._operationmode_actor,
            "antifreeze": self._antifreeze,
            "antifreeze_temp": self._antifreeze_temp,
            "firstopen_time": self._firstopen_time,
            "smartstart": self._smartstart,
            "eco_diff": self._eco_diff,
            "eco_inputmode": self._eco_inputmode,
            "eco_input_state": self._eco_input_state,
            "t_heat_vacation": self._t_heat_vacation
        }

    @autoupdate_property
    def id(self):
        return self._id

    @autoupdate_property
    def type(self):
        return self._type

    @autoupdate_property
    def name(self):
        return self._name

    @autoupdate_property
    def origin(self):
        return self._origin

    @autoupdate_property
    def errorcount(self):
        return self._errorcount

    @autoupdate_property
    def datetime(self):
        return self._datetime

    @autoupdate_property
    def dayofweek(self):
        return self._dayofweek

    @autoupdate_property
    def timezone(self):
        return self._timezone

    @autoupdate_property
    def ntptimesync(self):
        return self._ntptimesync

    @autoupdate_property
    def vers_sw_stm(self):
        return self._vers_sw_stm

    @autoupdate_property
    def vers_sw_eth(self):
        return self._vers_sw_eth

    @autoupdate_property
    def vers_hw(self):
        return self._vers_hw

    @autoupdate_property
    def temperatureunit(self):
        return self._temperatureunit

    @autoupdate_property
    def summerwinter(self):
        return self._summerwinter

    @autoupdate_property
    def tps(self):
        return self._tps

    @autoupdate_property
    def limiter(self):
        return self._limiter

    @autoupdate_property
    def masterid(self):
        return self._masterid

    @autoupdate_property
    def changeover(self):
        return self._changeover

    @autoupdate_property
    def cooling(self):
        return self._cooling

    @autoupdate_property
    def mode(self):
        return self._mode

    @autoupdate_property
    def operationmode_actor(self):
        return self._operationmode_actor

    @autoupdate_property
    def antifreeze(self):
        return self._antifreeze

    @autoupdate_property
    def antifreeze_temp(self):
        return self._antifreeze_temp

    @autoupdate_property
    def firstopen_time(self):
        return self._firstopen_time

    @autoupdate_property
    def smartstart(self):
        return self._smartstart

    @autoupdate_property
    def eco_diff(self):
        return self._eco_diff

    @autoupdate_property
    def eco_inputmode(self):
        return self._eco_inputmode

    @autoupdate_property
    def eco_input_state(self):
        return self._eco_input_state

    @autoupdate_property
    def t_heat_vacation(self):
        return self._t_heat_vacation

import time

from .const import HEATAREA_MODES
from .exceptions import RehauNeaSmartError
from .utils import autoupdate_property

class RehauNeaSmartHeatarea(object):
    def __init__(self, bridge, id, auto_update=True):
        self._id = id
        self._bridge = bridge
        self._last_refresh_time = 0
        self._auto_update = auto_update

    def _make_request(self, type='GET', request=None):
        if type == 'POST':
            request['id'] = self._id
            request['device'] = 'HEATAREA'
        return self._bridge._make_request(type=type, request=request)


    def _update_if_needed(self):
        """Check whether the existing status is too stale and update it if so."""
        if self._auto_update and time.time() - self._last_refresh_time >= 1:
            self._update_status()


    def _update_status(self):
        """Fetch the device's current status from the bridge."""
        status_line = self._make_request()

        for child in status_line.iter(tag='HEATAREA'):
            if child.attrib['nr'] == self._id:
                for subelem in child:
                    setattr(self, '_' + subelem.tag.lower(), subelem.text)


        self._last_refresh_time = time.time()

    def _clear_status(self):
        """Force the next property read to refresh the device status if
        autoupdate mode is active."""
        self._last_refresh_time = 0

    def update_status(self):
        """Force a status update. Normally, status is queried automatically
        if it hasn't been updated in the past second."""
        self._clear_status()
        self._update_status()

    @autoupdate_property
    def status(self):
        return {
            "heatarea_name": self._heatarea_name,
            "heatarea_mode": self._heatarea_mode,
            "t_actual": self._t_actual,
            "t_actual_ext": self._t_actual_ext,
            "t_target": self._t_target,
            "t_target_base": self._t_target_base,
            "heatarea_state": self._heatarea_state,
            "program_source": self._program_source,
            "program_week": self._program_week,
            "program_weekend": self._program_weekend,
            "party": self._party,
            "party_remainingtime": self._party_remainingtime,
            "presence": self._presence,
            "islocked": self._islocked
        }


    def set_t_target(self, value):
        """
        Usage:
            Set a new target temperature
        Args:
            value (integer / float): The requested temperature
        """
        request = {
            'value': float(value),
            'key': 'T_TARGET',
        }
        self._make_request(type='POST', request=request)
        self._clear_status()

    def set_heatarea_mode(self, value):
        """
        Usage:
            Set a new heatarea mode. See possibles values in args section

        Args:
            value (integer): 0 : AUTO / 1 : COMFORT / 2: ECO. Any other value will throw an error
        """

        if value not in HEATAREA_MODES:
            raise(RehauNeaSmartError('%s is not a valid heatarea_mode value. Please check the documentation' % value))

        request = {
            'value': value,
            'key': 'HEATAREA_MODE',
        }
        self._make_request(type='POST', request=request)
        self._clear_status()


    @autoupdate_property
    def heatarea_name(self):
        return self._heatarea_name

    @autoupdate_property
    def heatarea_mode(self):
        return self._heatarea_mode

    @autoupdate_property
    def t_actual(self):
        return float(self._t_actual)

    @autoupdate_property
    def t_actual_ext(self):
        return float(self._t_actual_ext)

    @autoupdate_property
    def t_target(self):
        return float(self._t_target)

    @autoupdate_property
    def t_target_base(self):
        return float(self._t_target_base)

    @autoupdate_property
    def heatarea_state(self):
        return self._heatarea_state

    @autoupdate_property
    def program_source(self):
        return self._program_source

    @autoupdate_property
    def program_week(self):
        return self._program_week

    @autoupdate_property
    def program_weekend(self):
        return self._program_weekend

    @autoupdate_property
    def party(self):
        return self._party

    @autoupdate_property
    def party_remainingtime(self):
        return self._party_remainingtime

    @autoupdate_property
    def presence(self):
        return self._presence

    @autoupdate_property
    def islocked(self):
        return self._islocked

    @property
    def id(self):
        return self._id

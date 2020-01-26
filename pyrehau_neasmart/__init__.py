#!/usr/bin/env python3
import re
import requests
import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

__author__ = "Jeoffrey Bauvin"

_MODES = ["auto", "day", "night"]
_PATH_GET = '/data/static.xml'
_PATH_POST = '/data/changes.xml'

def autoupdate_property(func):
    def update_and_get(*args):
        args[0]._update_if_needed()
        return func(*args)
    return property(update_and_get)

class RehauNeaSmart(object):
    def __init__(self, host, port=80, auto_update=True):
        """Initialize the Rehau NeaSmart instance."""
        self._host = host
        self._port = port
        self._auto_update = auto_update

    def _make_request(self, type='GET', request=None):
        print('New request %s' % (type))
        if type == 'GET':
            url = 'http://%s:%s%s' % (self._host, self._port, _PATH_GET)
            r = requests.get(url)
        elif type == 'POST':
            print('making a post request')
            url = 'http://%s:%s%s' % (self._host, self._port, _PATH_POST)
            headers = {
                'Accept': '*/*',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
            device = request['device']
            key = request['key']
            value = request['value']
            id = request['id']
            # TODO : build xml with elementree ?
            data = """<?xml version="1.0" encoding="UTF-8"?>
            <Devices>
                <Device>
                    <%s nr="%s">
                        <%s>%s</%s>
                    </%s>
                </Device>
            </Devices>""" % (device, id, key, value, key, device)
            r = requests.post(url, headers=headers, data=data)
        if r.status_code == 200:
            root = ET.fromstring(r.text)
            return root
        else:
            return False


    def heatareas(self):
        """Return a list of heatareas"""
        devices = []
        oneshot = self._make_request(type='GET')
        for child in oneshot.iter(tag='HEATAREA'):
            devices.append(RehauNeaSmartHeatarea(self, id=child.attrib['nr'], auto_update=self._auto_update))
        return devices


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
        request = {
            'value': value,
            'key': 'T_TARGET',
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

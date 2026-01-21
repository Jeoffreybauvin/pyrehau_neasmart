#!/usr/bin/env python3
import requests

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from .const import _PATH_GET, _PATH_POST
from .heatarea import RehauNeaSmartHeatarea
from .iodevice import RehauNeaSmartIoDevice
from .device import RehauNeaSmartDevice
from .exceptions import RehauNeaSmartError

__author__ = "Jeoffrey Bauvin"

class RehauNeaSmart(object):
    def __init__(self, host, port=80, auto_update=True):
        """
        Args:
            host (string): Rehau Nea Smart hostname (or IP)
            port (integer): default 80
            auto_update (boolean): enable auto update (need documentation)
        """
        self._host = host
        self._port = port
        self._auto_update = auto_update

    def _make_request(self, type='GET', request=None):
        print('New request %s' % (type))
        if type == 'GET':
            url = 'http://%s:%s%s' % (self._host, self._port, _PATH_GET)
            r = requests.get(url)
        elif type == 'POST':
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


    def get_heatarea(self, nr):
        """
        Args:
            nr (string): HEATAREA_NR
        Returns:
            RehauNeaSmartHeatarea object or None
        """
        oneshot = self._make_request(type='GET')
        if oneshot:
            for child in oneshot.iter(tag='HEATAREA'):
                if child.attrib['nr'] == str(nr):
                    return RehauNeaSmartHeatarea(self, id=child.attrib['nr'], auto_update=self._auto_update)
        return None

    def heatareas(self):
        """
        Returns:
            a list of heatareas
        """

        devices = []
        oneshot = self._make_request(type='GET')
        if oneshot:
            for child in oneshot.iter(tag='HEATAREA'):
                devices.append(RehauNeaSmartHeatarea(self, id=child.attrib['nr'], auto_update=self._auto_update))
        return devices

    def get_iodevice(self, nr):
        """
        Args:
            nr (string): IODEVICE_NR
        Returns:
            RehauNeaSmartIoDevice object or None
        """
        oneshot = self._make_request(type='GET')
        if oneshot:
            for child in oneshot.iter(tag='IODEVICE'):
                if child.attrib['nr'] == str(nr):
                    return RehauNeaSmartIoDevice(self, id=child.attrib['nr'], auto_update=self._auto_update)
        return None

    def iodevices(self):
        """
        Returns:
            a list of iodevices
        """

        devices = []
        oneshot = self._make_request(type='GET')
        if oneshot:
            for child in oneshot.iter(tag='IODEVICE'):
                devices.append(RehauNeaSmartIoDevice(self, id=child.attrib['nr'], auto_update=self._auto_update))
        return devices

    def device(self):
        """
        Returns:
            RehauNeaSmartDevice object representing the main controller
        """
        return RehauNeaSmartDevice(self, auto_update=self._auto_update)



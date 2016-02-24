#!/usr/bin/env python
# encoding: utf-8

from .vpn.manager import OpenVPN
from .firewall.manager import Firewall


class EIPManager(object):
    """
    The EIP Manager object, this handles the service actions and switch between
    states.
    """
    def __init__(self):
        self._firewall = Firewall()
        self._openvpn = OpenVPN()

    def status(self):
        pass

    def start(self):
        self._firewall.start()
        pass

    def stop(self):
        pass

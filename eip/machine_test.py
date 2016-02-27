#!/usr/bin/env python
# encoding: utf-8

from .vpn.machine_test import VPNMachine
from .firewall.machine_test import FirewallMachine


class EIPMachine(object):
    """
    The EIP Manager object, this handles the service actions and switch between
    states.
    """
    def __init__(self):
        self._firewall = FirewallMachine()
        self._vpn = VPNMachine()

    def status(self):
        pass

    def _eip_on(self):
        print "EIP IS ON"

    def _start_vpn(self):
        print "Firewall is on, starting VPN"
        self._vpn.set_callback('start_ok', self._eip_on)
        self._vpn.start()

    def start(self):
        self._firewall.set_callback('start_ok', self._start_vpn)
        self._firewall.start()

    def stop(self):
        pass


def main():
    em = EIPMachine()
    em.start()


if __name__ == "__main__":
    main()

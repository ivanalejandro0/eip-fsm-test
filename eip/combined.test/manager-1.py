#!/usr/bin/env python
# encoding: utf-8

import random

from .eip_machine import EIPMachine


def random_failure(name):
    if random.randint(0, 5) == 0:
        raise Exception("{0}: some imaginary failure.".format(name))


class OpenVPN(object):
    def start(self):
        random_failure("OpenVPN - start")

    def stop(self):
        random_failure("OpenVPN - stop")


class Firewall(object):
    def start(self):
        random_failure("Firewall - start")

    def stop(self):
        random_failure("Firewall - stop")


class EIPManager(object):
    """
    The EIP Manager object, this handles the service actions and switch between
    states.
    """
    def __init__(self):
        self._statemachine = EIPMachine()
        self._firewall = Firewall()
        self._openvpn = OpenVPN()

    def status(self):
        return self._statemachine.state

    def start(self):
        """Start the EIP service.

        :returns: True if succeed, False otherwise
        :rtype: bool"""
        self._statemachine.start()

        try:
            self._firewall.start()
        except Exception as e:
            print "Problem: {0!r}".format(e)
            self._statemachine.fw_error()
            return False

        self._statemachine.fw_ok()

        try:
            self._openvpn.start()
        except Exception as e:
            print "Problem: {0!r}".format(e)
            self._statemachine.eip_error()
            return False

        self._statemachine.eip_ok()
        return True

    def stop(self):
        """Stop the EIP service.

        :returns: True if succeed, False otherwise
        :rtype: bool"""
        self._statemachine.stop()

        try:
            self._openvpn.stop()
        except Exception as e:
            print "Problem: {0!r}".format(e)
            self._statemachine.eip_stop_error()
            return False

        self._statemachine.eip_stop_ok()

        try:
            self._firewall.stop()
        except Exception as e:
            print "Problem: {0!r}".format(e)
            self._statemachine.fw_stop_error()
            return False

        self._statemachine.fw_stop_ok()
        return True

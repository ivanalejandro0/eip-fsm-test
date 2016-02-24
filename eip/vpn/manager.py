#!/usr/bin/env python
# encoding: utf-8

import random

from .machine import VPNMachine


def random_failure(name):
    if random.randint(0, 3) != 0:
        raise Exception("{0}: some imaginary failure.".format(name))


class OpenVPN(object):
    RETRIES = 3

    def __init__(self):
        self._statemachine = VPNMachine()

    def _start(self):
        random_failure("start")

    def start(self, retries=RETRIES):
        self._statemachine.start()

        for i in xrange(1, retries+1):
            try:
                self._start()
                self._statemachine.start_ok()
                return True
            except:
                if i < retries:
                    print ("vpn: Problem starting... attempt {0} of {1}"
                           .format(i, retries))
                    self._statemachine.start_error()
                else:
                    print "vpn: Problem starting... error"
                    self._statemachine.failed()

    def stop(self):
        self._statemachine.stop()
        try:
            random_failure("stop")
            self._statemachine.stop_ok()
            return True
        except:
            self._statemachine.stop_error()

    def status(self):
        return self._statemachine.state

    # TODO: add states to react to stdout changes
    signals = {
        "network_unreachable": sig.eip_network_unreachable,
        "process_restart_tls": sig.eip_process_restart_tls,
        "process_restart_ping": sig.eip_process_restart_ping,
        "initialization_completed": sig.eip_connected
    }
    _events = {
        'NETWORK_UNREACHABLE': (
            'Network is unreachable (code=101)',),
        'PROCESS_RESTART_TLS': (
            "SIGTERM[soft,tls-error]",),
        'PROCESS_RESTART_PING': (
            "SIGTERM[soft,ping-restart]",),
        'INITIALIZATION_COMPLETED': (
            "Initialization Sequence Completed",),
    }

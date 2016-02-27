#!/usr/bin/env python
# encoding: utf-8

import random
import threading
import time

# TODO: add states to react to stdout changes, and state/status responses
_signals = {
    "network_unreachable": "the_qt_signaler.eip_network_unreachable",
    "process_restart_tls": "the_qt_signaler.eip_process_restart_tls",
    "process_restart_ping": "the_qt_signaler.eip_process_restart_ping",
    "initialization_completed": "the_qt_signaler.eip_connected",
}

_events = {
    'NETWORK_UNREACHABLE': ('Network is unreachable (code=101)',),
    'PROCESS_RESTART_TLS': ("SIGTERM[soft,tls-error]",),
    'PROCESS_RESTART_PING': ("SIGTERM[soft,ping-restart]",),
    'INITIALIZATION_COMPLETED': ("Initialization Sequence Completed",),
}


def random_failure(name):
    if random.randint(0, 1) != 0:
        raise Exception("{0}: some imaginary failure.".format(name))


class VPNManager(object):
    """
    Async OpenVPN manager, returns immediately on every call.
    Accepts callbacks to be notified right after some events occurs.
    """

    def __init__(self):
        self._call_on_start = None
        self._call_on_fail = None

    def _start(self):
        print "[openvpn] RUNNING VPN MAGIC..."
        time.sleep(1)
        started = False
        try:
            random_failure("openvpn - start")
            started = True
        except:
            started = False

        if started and callable(self._call_on_start):
            self._call_on_start()

        if not started and callable(self._call_on_fail):
            self._call_on_fail()

    def start(self, call_on_start=None, call_on_fail=None):
        self._call_on_start = call_on_start
        self._call_on_fail = call_on_fail
        self._start_thread = threading.Thread(target=self._start)
        self._start_thread.start()

    def stop(self):
        pass

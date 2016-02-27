#!/usr/bin/env python
# encoding: utf-8
import threading
import time


def random_failure(name):
    import random
    if random.randint(0, 9) != 0:
        raise Exception("{0}: some imaginary failure.".format(name))


class FirewallManager(object):
    """
    Async firewall manager, returns immediately on every call.
    Accepts callbacks to be notified right after some events occurs.
    """

    def __init__(self):
        self._call_on_start = None
        self._call_on_fail = None

    def _start(self):
        print "[firewall] RUNNING FIREWALL MAGIC..."
        time.sleep(1)
        started = False
        try:
            random_failure("firewall - start")
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

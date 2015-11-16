#!/usr/bin/env python
# encoding: utf-8

import random

from .machine import FirewallMachine


def random_failure(name):
    if random.randint(0, 3) != 0:
        raise Exception("{0}: some imaginary failure.".format(name))


class Firewall(object):
    RETRIES = 3

    def __init__(self):
        self._statemachine = FirewallMachine()

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
                    print ("firewall: Problem starting... attempt {0} of {1}"
                           .format(i, retries))
                    self._statemachine.start_error()
                else:
                    print "firewall: Problem starting... error"
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

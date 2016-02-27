#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine implementation for the Firewall service.
"""
import threading
import time

import xworkflows

import colorama
from colorama import Fore

from .workflow import FirewallWorkflow


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


class FirewallMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = FirewallWorkflow()
    MAX_RETRIES_DEFAULT = 3

    def __init__(self, retries=MAX_RETRIES_DEFAULT):
        self._firewall = FirewallManager()
        self._retry_count = 0
        self.MAX_RETRIES = retries

    # ---------- helper methods ----------
    def _print_state(self, color=None):
        if color is not None:
            print color + "[firewall] [S] entered: '{0}'".format(
                self.state.name) + Fore.RESET
            return

        print "[firewall] [S] entered: '{0}'".format(self.state.name)

    def _print_transition(self, name, color=None):
        if color is not None:
            print color + "[firewall] [T] triggered: '{0}'".format(
                name) + Fore.RESET
            return

        print "[firewall] [T] triggered: '{0}'".format(name)

    # ---------- transitions: log/notify here ----------
    @xworkflows.transition()
    def start(self):
        self._print_transition('start')

    @xworkflows.transition()
    def start_error(self):
        self._print_transition('start_error', Fore.YELLOW)

    @xworkflows.transition()
    def start_failed(self):
        self._print_transition('start_failed', Fore.RED)

    @xworkflows.transition()
    def start_ok(self):
        self._print_transition('start_ok', Fore.GREEN)

    @xworkflows.transition()
    def reset(self):
        self._print_transition('reset')
        self._retry_count = 0

    # ---------- states: do stuff here ----------
    @xworkflows.on_enter_state('off')
    def on_off(self, *args, **kwargs):
        self._print_state()

    @xworkflows.on_enter_state('starting')
    def starting(self, *args, **kwargs):
        self._print_state()
        self._firewall.start(self.start_ok, self.start_error)

    @xworkflows.on_enter_state('on')
    def on_on(self, *args, **kwargs):
        self._print_state(Fore.GREEN)

    @xworkflows.on_enter_state('error')
    def on_error(self, *args, **kwargs):
        self._print_state(Fore.RED)
        self.reset()

    @xworkflows.on_enter_state('retrying')
    def on_retrying(self, *args, **kwargs):
        self._print_state(Fore.YELLOW)

        if self._retry_count < self.MAX_RETRIES:
            self._retry_count += 1
            print "[firewall] retrying, attempt {0} of {1}".format(
                self._retry_count, 3)
            self._firewall.start(self.start_ok, self.start_retry_error)
        else:
            self._firewall.start(self.start_ok, self.start_failed)


def main():
    colorama.init()
    print "[main] firewall machine test"
    fm = FirewallMachine()
    fm.start()


if __name__ == "__main__":
    main()

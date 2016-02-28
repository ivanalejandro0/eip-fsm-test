#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine implementation for the Firewall service.
"""
import xworkflows

import colorama
from colorama import Fore

from .workflow import FirewallWorkflow
from .manager_test import FirewallManager
from .publisher import ZMQPublisher


class FirewallMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = FirewallWorkflow()
    MAX_RETRIES_DEFAULT = 3

    def __init__(self, retries=MAX_RETRIES_DEFAULT):
        self.MAX_RETRIES = retries
        self._retry_count = 0

        self._pub = ZMQPublisher()
        self._pub.start()

        self._firewall = FirewallManager()
        self._callbacks = {}

    # ---------- helper methods ----------
    def _log(self, data, color=None):
        if color is not None:
            print color + data + Fore.RESET
        else:
            print data

        self._pub.send(data)

    def _log_state(self, color=None):
        msg = "[firewall] [S] entered: '{0}'".format(self.state.name)
        self._log(msg, color)

    def _log_transition(self, name, color=None):
        msg = "[firewall] [T] triggered: '{0}'".format(name)
        self._log(msg)

        callback = self._callbacks.pop(name, None)
        if callback is not None:
            callback()

    def set_callback(self, name, callme):
        if not callable(callme):
            raise TypeError("Argument should be callable")

        self._callbacks[name] = callme

    # ---------- transitions: log/notify here ----------
    @xworkflows.transition()
    def start(self):
        self._log_transition('start')

    @xworkflows.transition()
    def start_error(self):
        self._log_transition('start_error', Fore.YELLOW)

    @xworkflows.transition()
    def start_failed(self):
        self._log_transition('start_failed', Fore.RED)

    @xworkflows.transition()
    def start_ok(self):
        self._log_transition('start_ok', Fore.GREEN)

    @xworkflows.transition()
    def reset(self):
        self._log_transition('reset')
        self._retry_count = 0

    # ---------- states: do stuff here ----------
    @xworkflows.on_enter_state('off')
    def on_off(self, *args, **kwargs):
        self._log_state()

    @xworkflows.on_enter_state('starting')
    def starting(self, *args, **kwargs):
        self._log_state()
        self._firewall.start(self.start_ok, self.start_error)

    @xworkflows.on_enter_state('on')
    def on_on(self, *args, **kwargs):
        self._log_state(Fore.GREEN)
        self._pub.stop()

    @xworkflows.on_enter_state('error')
    def on_error(self, *args, **kwargs):
        self._log_state(Fore.RED)
        self.reset()
        self._pub.stop()

    @xworkflows.on_enter_state('retrying')
    def on_retrying(self, *args, **kwargs):
        self._log_state(Fore.YELLOW)

        if self._retry_count < self.MAX_RETRIES:
            self._retry_count += 1
            self._log("[firewall] retrying, attempt {0} of {1}".format(
                self._retry_count, self.MAX_RETRIES))
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

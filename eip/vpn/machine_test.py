#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine implementation for the Firewall service.
"""
import xworkflows

import colorama
from colorama import Fore

from .workflow import VPNWorkflow
from .manager_test import VPNManager


class VPNMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = VPNWorkflow()
    MAX_RETRIES_DEFAULT = 3

    def __init__(self, retries=MAX_RETRIES_DEFAULT):
        self._vpn = VPNManager()
        self._retry_count = 0
        self.MAX_RETRIES = retries

    # ---------- helper methods ----------
    def _print_state(self, color=None):
        if color is not None:
            print color + "[vpn] [S] entered: '{0}'".format(
                self.state.name) + Fore.RESET
            return

        print "[vpn] [S] entered: '{0}'".format(self.state.name)

    def _print_transition(self, name, color=None):
        if color is not None:
            print color + "[vpn] [T] triggered: '{0}'".format(
                name) + Fore.RESET
            return

        print "[vpn] [T] triggered: '{0}'".format(name)

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
        self._vpn.start(self.start_ok, self.start_error)

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
            print "[vpn] retrying, attempt {0} of {1}".format(
                self._retry_count, self.MAX_RETRIES)
            self._vpn.start(self.start_ok, self.start_retry_error)
        else:
            self._vpn.start(self.start_ok, self.start_failed)


def main():
    colorama.init()
    print "[main] vpn machine test"
    vm = VPNMachine()
    vm.start()


if __name__ == "__main__":
    main()

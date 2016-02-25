#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine implementation for the Firewall service.
"""
import time

import xworkflows

from .workflow import FirewallWorkflow


def random_failure(name):
    import random
    if random.randint(0, 3) != 0:
        raise Exception("{0}: some imaginary failure.".format(name))


# TODO think
# vpn/firewall stuff (the actual code) on states or transitions?
# maybe actions on states and notifications on transitions


class FirewallMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = FirewallWorkflow()

    # @xworkflows.transition()
    # def start(self):
    #     random_failure("Firewall - start")
    #     time.sleep(1)
    #     self.start_ok()
    #
    # @xworkflows.transition()
    # def stop(self):
    #     random_failure("Firewall - stop")
    #
    # @xworkflows.transition()
    # def cancel(self):
    #     random_failure("Firewall - cancel")

    def __init__(self):
        self._firewall_started = False
        self._retry_count = 0

    def _start_firewall(self):
        print "[firewall] RUNNING FIREWALL MAGIC..."
        time.sleep(1)
        try:
            random_failure("firewall - start")
            return True  # firewall started
        except:
            return False  # firewall not started

    def _print_state(self):
        print "[firewall] entered: '{0}'".format(self.state.name)

    @xworkflows.transition()
    def start(self):
        print "[firewall] start transition"

    @xworkflows.on_enter_state('starting')
    def starting(self, *args, **kwargs):
        self._print_state()
        self._firewall_started = self._start_firewall()
        if self._firewall_started:
            self.start_ok()
        else:
            self.start_error()

    @xworkflows.on_enter_state('on')
    def on_on(self, *args, **kwargs):
        self._print_state()

    @xworkflows.transition()
    def start_error(self):
        self._start_firewall()

    @xworkflows.on_enter_state('retrying')
    def on_retrying(self, *args, **kwargs):
        print "[firewall] entered: '{0}'".format(self.state.name)
        import random
        if random.randint(0, 2) != 0:
            if self._retry_count < 3:
                self._retry_count += 1
                print "[firewall] retrying, attempt {0} of {1}".format(
                    self._retry_count, 3)
                self.start_error()
            else:
                self.failed()
        else:
            self.start_ok()


def main():
    print "[main] firewall machine test"
    fm = FirewallMachine()
    fm.start()
    print "[main] state: ", fm.state


if __name__ == "__main__":
    main()

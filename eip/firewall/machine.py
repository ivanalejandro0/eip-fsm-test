#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine implementation for the Firewall service.
"""
# import time

import xworkflows

from .workflow import FirewallWorkflow


def random_failure(name):
    import random
    if random.randint(0, 5) == 0:
        raise Exception("{0}: some imaginary failure.".format(name))


class FirewallMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = FirewallWorkflow()

    # @xworkflows.transition()
    # def start(self):
    #     random_failure("Firewall - start")
    #     time.sleep(1)
    #     self.firewall_ok()
    #
    # @xworkflows.transition()
    # def stop(self):
    #     random_failure("Firewall - stop")
    #
    # @xworkflows.transition()
    # def cancel(self):
    #     random_failure("Firewall - cancel")

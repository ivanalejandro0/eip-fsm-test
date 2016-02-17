#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine for the VPN service.
"""
import xworkflows

from .workflow import VPNWorkflow


def random_failure(name):
    import random
    if random.randint(0, 5) == 0:
        raise Exception("{0}: some imaginary failure.".format(name))


class VPNMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = VPNWorkflow()

    # @xworkflows.transition()
    # def start(self):
    #     random_failure("VPN - start")
    #     time.sleep(1)
    #     self.start_ok()
    #
    # @xworkflows.transition()
    # def stop(self):
    #     random_failure("VPN - stop")
    #
    # @xworkflows.transition()
    # def cancel(self):
    #     random_failure("VPN - cancel")

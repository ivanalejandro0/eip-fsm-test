#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine for the Firewall service.
"""
import xworkflows


class FirewallWorkflow(xworkflows.Workflow):
    """
    VPN workflow definition of states and transitions.
    """

    states = (
        ('off', "The Firewall is off"),
        ('on', "The Firewall is on"),
        ('error', "Fatal error, can't recover."),

        ('firewall_starting', "Firewall is starting."),
        ('firewall_stopping', "Firewall is stopping."),
        ('firewall_retrying', "Retrying Firewall start."),
        ('firewall_failed', "Gave up on Firewall, may be tried again."),
    )

    transitions = (
        ('start', 'off', 'firewall_starting'),

        ('firewall_ok', 'firewall_starting', 'on'),
        ('firewall_cancel', 'firewall_starting', 'firewall_stopping'),
        ('firewall_error', 'firewall_starting', 'firewall_retrying'),
        ('firewall_retry_error', 'firewall_retrying', 'firewall_retrying'),
        ('firewall_failed', 'firewall_retrying', 'error'),

        ('stop', 'on', 'firewall_stopping'),

        ('firewall_stop_ok', 'firewall_stopping', 'off'),
        ('firewall_stop_error', 'firewall_stopping', 'error'),

        ('reset', 'error', 'off'),
    )

    initial_state = 'off'


def random_failure(name):
    import random
    if random.randint(0, 5) == 0:
        raise Exception("{0}: some imaginary failure.".format(name))


class FirewallMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = FirewallWorkflow()

    @xworkflows.transition()
    def start(self):
        random_failure("Firewall - start")
        pass

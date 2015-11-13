#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine for the EIP service, based on
https://leap.se/code/issues/5616#note-2
"""
import xworkflows


class EIPWorkflow(xworkflows.Workflow):
    """
    EIP workflow definition of states and transitions.
    """

    states = (
        ('off', "Everything is off"),
        ('on', "Everything is on"),
        ('error', "Fatal error, can't recover."),

        ('firewall_starting', "Firewall is starting."),
        ('firewall_stopping', "firewall is stopping."),

        ('eip_starting', "OpenVPN is starting."),
        ('eip_stopping', "OpenVPN is stopping."),
        ('eip_retrying', "Retrying OpenVPN start."),
        ('eip_failed', "Gave up on OpenVPN, may be tried again."),
    )

    transitions = (
        ('start', 'off', 'firewall_starting'),

        ('firewall_ok', 'firewall_starting', 'eip_starting'),
        ('firewall_error', 'firewall_starting', 'error'),

        ('eip_ok', 'eip_starting', 'on'),
        ('eip_cancel', 'eip_starting', 'eip_stopping'),
        ('eip_error', 'eip_starting', 'eip_retrying'),
        ('eip_failed', 'eip_retrying', 'error'),

        ('stop', 'on', 'eip_stopping'),

        ('eip_stop_ok', 'eip_stopping', 'firewall_stopping'),
        ('eip_stop_error', 'eip_stopping', 'error'),

        ('firewall_stop_ok', 'firewall_stopping', 'off'),
        ('firewall_stop_error', 'firewall_stopping', 'error'),

        ('reset', 'error', 'off'),
    )

    initial_state = 'off'


class EIPMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = EIPWorkflow()

    @xworkflows.transition()
    def start(self):
        pass

#!/usr/bin/env python
# encoding: utf-8
"""
A Finite State Machine for the VPN service.
"""
import xworkflows


class VPNWorkflow(xworkflows.Workflow):
    """
    VPN workflow definition of states and transitions.
    """

    states = (
        ('off', "The VPN is off"),
        ('on', "The VPN is on"),
        ('error', "Fatal error, can't recover."),

        ('vpn_starting', "OpenVPN is starting."),
        ('vpn_stopping', "OpenVPN is stopping."),
        ('vpn_retrying', "Retrying OpenVPN start."),
        ('vpn_failed', "Gave up on OpenVPN, may be tried again."),
    )

    transitions = (
        ('start', 'off', 'vpn_starting'),

        ('vpn_ok', 'vpn_starting', 'on'),
        ('vpn_cancel', 'vpn_starting', 'vpn_stopping'),
        ('vpn_error', 'vpn_starting', 'vpn_retrying'),
        ('vpn_retry_error', 'vpn_retrying', 'vpn_retrying'),
        ('vpn_failed', 'vpn_retrying', 'error'),

        ('stop', 'on', 'vpn_stopping'),

        ('vpn_stop_ok', 'vpn_stopping', 'off'),
        ('vpn_stop_error', 'vpn_stopping', 'error'),

        ('reset', 'error', 'off'),
    )

    initial_state = 'off'


class VPNMachine(xworkflows.WorkflowEnabled):
    """
    The actual state machine to be used to do the transitions and check states.
    """
    state = VPNWorkflow()

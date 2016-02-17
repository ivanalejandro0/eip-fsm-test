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

        ('starting', "OpenVPN is starting."),
        ('stopping', "OpenVPN is stopping."),
        ('retrying', "Retrying OpenVPN start."),
        ('failed', "Gave up on OpenVPN, may be tried again."),
    )

    transitions = (
        ('start', 'off', 'vpn_starting'),

        ('start_ok', 'starting', 'on'),
        ('start_cancel', 'starting', 'stopping'),
        ('start_error', 'starting', 'retrying'),
        ('start_retry_error', 'retrying', 'retrying'),
        ('start_failed', 'retrying', 'error'),

        ('stop', 'on', 'stopping'),

        ('stop_ok', 'stopping', 'off'),
        ('stop_error', 'stopping', 'error'),

        ('reset', 'error', 'off'),
    )

    initial_state = 'off'

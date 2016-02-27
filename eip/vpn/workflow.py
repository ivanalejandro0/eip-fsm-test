#!/usr/bin/env python
# encoding: utf-8
"""
Finite State Machine worlflow definition for the VPN service.
"""
import xworkflows


class VPNWorkflow(xworkflows.Workflow):
    """
    VPN workflow definition of states and transitions.
    """

    states = (
        ('off', "The VPN is off"),
        ('on', "The VPN is on"),
        ('error', "Can't start VPN."),

        ('starting', "OpenVPN is starting."),
        ('stopping', "OpenVPN is stopping."),
        ('retrying', "Retrying OpenVPN start."),
    )

    transitions = (
        ('start', 'off', 'starting'),

        ('start_ok', ('starting', 'retrying'), 'on'),
        ('start_error', 'starting', 'retrying'),
        ('start_cancel', 'starting', 'stopping'),
        ('start_retry_error', 'retrying', 'retrying'),
        ('start_failed', 'retrying', 'error'),

        ('stop', 'on', 'stopping'),

        ('stop_ok', 'stopping', 'off'),
        ('stop_error', 'stopping', 'error'),

        ('reset', 'error', 'off'),
    )

    initial_state = 'off'

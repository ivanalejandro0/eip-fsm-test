#!/usr/bin/env python
# encoding: utf-8
"""
Finite State Machine worlflow definition for the Firewall service.
"""
import xworkflows


class FirewallWorkflow(xworkflows.Workflow):
    """
    Firewall workflow definition of states and transitions.
    """

    states = (
        ('off', "The Firewall is off"),
        ('on', "The Firewall is on"),
        ('error', "Can't start firewall."),

        ('starting', "Firewall is starting."),
        ('stopping', "Firewall is stopping."),
        ('retrying', "Retrying Firewall start."),
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

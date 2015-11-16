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
        ('error', "Fatal error, can't recover."),

        ('starting', "Firewall is starting."),
        ('stopping', "Firewall is stopping."),
        ('retrying', "Retrying Firewall start."),
        ('failed', "Gave up on Firewall, may be tried again."),
    )

    transitions = (
        ('start', 'off', 'starting'),

        ('start_ok', ('starting', 'retrying'), 'on'),
        ('start_error', ('starting', 'retrying'), 'retrying'),
        ('start_cancel', 'starting', 'stopping'),
        ('failed', 'retrying', 'error'),

        ('stop', 'on', 'stopping'),

        ('stop_ok', 'stopping', 'off'),
        ('stop_error', 'stopping', 'error'),

        ('reset', 'error', 'off'),
    )

    initial_state = 'off'

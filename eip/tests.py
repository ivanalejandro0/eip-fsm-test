#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from pprint import pprint

from .machine import EIPMachine
from .manager import EIPManager


def debug():
    """
    This shows us some details about the internals of the xworkflows object.
    """
    em = EIPMachine()

    print dir(em)
    print
    print dir(em.state)
    print
    pprint(list(em.state.transitions()))
    print


def simple_test():
    """A simple test of the transitions/states"""
    em = EIPMachine()

    print em.state.title
    em.start()
    print em.state.title
    em.fw_ok()
    print em.state.title
    em.eip_error()
    print em.state.title
    em.eip_failed()
    print em.state.title


def test_eip_manager():
    eip_manager = EIPManager()
    if eip_manager.start():
        print "EIP is started"
    else:
        print "EIP has failed starting - reached state:", eip_manager.status()


def test_random_paths():
    """
    This run a random sequence of valid transitions for each state until
    reaches a final state (error/on) or no more transitions can be done.
    """
    em = EIPMachine()

    # go randomly through available transitions
    retries = 0
    max_retries = 3
    while retries <= max_retries:
        try:
            # get available transitions from here
            ts = list(em.state.transitions())

            state = em.state.name
            print "State:", state

            # Stop in case of final state reached
            if state == 'error':
                retries += 1
                if retries <= max_retries:
                    print "Retrying!"

            if state == 'on':
                print "-"*50
                print "Final state reached. ON"
                break

            if len(ts) == 0:
                print "-"*50
                print "ERROR: no available transitions. State:", state
                break

            # pick one transition randomly
            random.shuffle(ts)
            transition = ts[0].name

            # do the transition
            t = em.__getattribute__(transition)
            t()
        except Exception as e:
            print "Exception caught:", repr(e)

    if state == 'error':
        print "-"*50
        print "Final state reached. Error"


if __name__ == '__main__':
    # test_random_paths()
    test_eip_manager()

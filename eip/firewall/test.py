#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from .machine import FirewallMachine
from .manager import Firewall


def test_1():
    fm = Firewall()

    up = fm.start()
    if up:
        print "manager: firewall started"
    else:
        print "manager: firewall failed starting - reached state:", fm.status()

    if not up:
        print "manager: firewall not started, won't try to stop it"
        return

    if fm.stop():
        print "manager: firewall stopped"
    else:
        print "manager: firewall failed stopping - reached state:", fm.status()


if __name__ == "__main__":
    test_1()

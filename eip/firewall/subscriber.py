#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading

import zmq


class ZMQSubscriber(object):
    def __init__(self):
        self._worker_thread = threading.Thread(target=self._run)
        self._do_work = threading.Event()

    def start(self):
        """
        Start the worker thread for the signaler server.
        """
        self._do_work.set()
        self._worker_thread.start()

    def _run(self):
        """
        Start a loop to process the ZMQ requests from the signaler client.
        """
        print "ZMQSubscriber: loop started"
        port = "5556"
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:%s" % port)
        # socket.setsockopt_string(zmq.SUBSCRIBE, u'')  # get everything
        socket.setsockopt_string(zmq.SUBSCRIBE, u'[firewall]')
        socket.setsockopt_string(zmq.SUBSCRIBE, u'END')

        while self._do_work.is_set():
            try:
                data = socket.recv_string()
                # print "Got data:", repr(data)
                print data
                if data == 'END':
                    self.stop()
            except Queue.Empty:
                pass

        print "ZMQSubscriber: loop stopped"

    def stop(self):
        """
        Stop the SignalerQt blocking loop.
        """
        self._do_work.clear()


def main():
    # Ensure that the application quits using CTRL-C
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sub = ZMQSubscriber()
    sub.start()

if __name__ == "__main__":
    main()

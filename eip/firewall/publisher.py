#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading
import time

import zmq


class ZMQPublisher(object):
    def __init__(self):
        self._worker_thread = threading.Thread(target=self._run)
        self._do_work = threading.Event()
        self._queue = Queue.Queue()

    def start(self):
        """
        Start the worker thread for the signaler server.
        """
        self._do_work.set()
        self._worker_thread.start()

    def send(self, data):
        self._queue.put(data)

    def _run(self):
        """
        Start a loop to process the ZMQ requests from the signaler client.
        """
        print "ZMQPublisher: loop started"

        port = "5556"
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:%s" % port)

        while self._do_work.is_set():
            try:
                data = self._queue.get(timeout=0.1)
                # print "Got data from queue: ", data
                socket.send_string(data)
            except Queue.Empty:
                pass

        print "ZMQPublisher: loop stopped"

    def stop(self):
        """
        Stop the SignalerQt blocking loop.
        """
        self.send('END')
        time.sleep(.1)
        self._do_work.clear()

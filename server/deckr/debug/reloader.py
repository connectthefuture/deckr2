# pylint: skip-file
"""
This module provides code for reloading services for quicker development. Essentially it spnis off each service
into a seperate process and then communicates between them using xmlrpc. If there are any file changes detected
it will restart the process which forces a reload of all modules.

Note:
    This is not foolproof and can get kind of messy. With the reloader you'll have processes, threads, and
    probably the twisted event loop. Shutting down doesn't currently work properly so you just need to kill it
    if you want a full shutdown.
"""

import logging
import multiprocessing
import os.path
import SimpleXMLRPCServer
import sys
import threading
import time
import xmlrpclib

import deckr.core.service_wrapper

LOGGER = logging.getLogger(__name__)

NEXT_PORT = 10000  # Port to start the next service XMLRPC server on


class ReloadingServiceWrapper(deckr.core.service_wrapper.ServiceWrapper):
    """
    This handles all of the reloading logic. It handles file watching, process reloading, and
    transparent proxying. This implements the same interface as a ServiceWrapper.
    """

    def __init__(self, service_config, config_for_service=None):
        super(ReloadingServiceWrapper, self).__init__(
            service_config, config_for_service)
        self._process = None
        self._file_watcher = FileWatcher(
            service_config.get("watch_files", []), self.reload)
        self._watcher_thread = None
        self._stopped = True
        # What port should we serve this on?
        global NEXT_PORT
        self._port = NEXT_PORT
        NEXT_PORT += 1

    def create(self):
        """
        Create the service and wrap it in an XMLRPC proxy.

        Returns:
            ReloaderProxy: A proxy that can be called as if it were the original class.
        """

        self._process = multiprocessing.Process(target=self._child_create)
        self._process.start()
        time.sleep(0.1)  # Make sure we give the proxy time to start up.

        self._instance = xmlrpclib.ServerProxy(
            "http://localhost:%d/" % self._port,
            allow_none=True)
        self._watcher_thread = threading.Thread(
            target=self._file_watcher.watch)
        self._watcher_thread.start()
        self._stopped = False

        return self._instance

    def stop(self):
        """
        Properly stop the reloading.
        """

        LOGGER.info("Stopping service: %s", self.name)
        self._process.terminate()
        self._file_watcher.done = True
        self._watcher_thread.join()
        self._stopped = True

    def _child_create(self):
        """
        Create in the child process.
        """

        instance = super(ReloadingServiceWrapper, self).create()
        LOGGER.info("Starting XMLRPCServer on localhost:%s", self._port)
        server = SimpleXMLRPCServer.SimpleXMLRPCServer(
            ("localhost", self._port),
            allow_none=True,
            logRequests=False)
        server.register_instance(instance)
        server.serve_forever()

    def reload(self):
        """
        Signal that we should reload and restart the service.
        """

        LOGGER.info("Reloading service: %s", self.name)
        self._process.terminate()
        self._process = multiprocessing.Process(target=self._child_create)
        self._process.start()
        time.sleep(0.1)  # Give the server time to start up

        self._instance.start()  # Restart our instance

    def __del__(self):
        if not self._stopped:
            self.stop()


class FileWatcher(object):
    """
    This class can watch a set of files for changes. If there are any changes it will trigger
    a callback.
    """

    FILE_POLL_SECONDS = 1

    def __init__(self, files, callback):
        self._files = files
        self._callback = callback
        self._last_modification_times = []
        self.done = False

    def watch(self):
        """
        Start watchin files. Will continue to watch until self.done is turned to false.
        """

        # Make sure we initialze to a good state
        self._last_modification_times = self.get_modification_times()

        while not self.done:
            time.sleep(self.FILE_POLL_SECONDS)
            modification_times = self.get_modification_times()
            if modification_times != self._last_modification_times:
                self._callback()
            self._last_modification_times = modification_times

    def get_modification_times(self):
        """
        Get the current modification times.
        """
        return [(x, os.path.getmtime(x)) for x in self._files]

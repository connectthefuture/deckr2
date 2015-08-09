"""
This module provides code for relodaing services in development. Essentially we wrap each service
in a seperate process and then proxy between them using queues. This way, we can kill a process and
restart it (forcing a code reload) without anybody else noticing.

Note:
    This is not foolproof. Your milage may vary.
"""


import logging
import os.path
import threading  # For file watcher
import time
from multiprocessing import Process, Queue  # For actual reloader

from deckr.services.service_wrapper import ServiceWrapper

LOGGER = logging.getLogger(__name__)


class ReloadingServiceWrapper(ServiceWrapper):
    """
    This handles all of the reloading logic. It handles file watching, process reloading, and
    transparent proxying. This implements the same interface as a ServiceWrapper.
    """

    def __init__(self, service_config, config_for_service=None):
        super(ReloadingServiceWrapper, self).__init__(
            service_config, config_for_service)
        self._process = None
        self._queue1 = Queue()
        self._queue2 = Queue()
        self._file_watcher = FileWatcher(
            service_config.get("watch_files", []), self.reload)
        self._watcher_thread = None
        self._stopped = True

    def create(self):
        """
        Create the service and wrap it in the ReoladerProxy.

        Returns:
            ReloaderProxy: A proxy that can be called as if it were the original class.
        """

        self._instance = ReloaderProxy(self._queue1, self._queue2)
        self._process = Process(target=self._child_create)
        self._process.start()
        # Start a new thread (has to be a thread instead of a process) to track
        # file changes
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
        Create in the child.
        """

        instance = super(ReloadingServiceWrapper, self).create()
        proxy = ReloaderProxy(self._queue2, self._queue1, instance)
        proxy.reloder_proxy_listen()

    def reload(self):
        """
        Signal that we should reload and restart the service.
        """

        LOGGER.info("Reloading service: %s", self.name)
        self._process.terminate()
        self._process = Process(target=self._child_create)
        self._process.start()
        self._instance.start()

    def __del__(self):
        if not self._stopped:
            self.stop()


class ReloaderProxy(object):
    """
    This represents a proxy object. If on the sending end it's returned as a normal object. If
    it's on the reciving end it will invoke _listen and wait until it's killed through KILL
    message.
    """

    def __init__(self, send_queue, recieve_queue, proxy_for=None):
        #: Queue for sending messages
        self._send_queue = send_queue
        #: Queue for recieving responses
        self._recieve_queue = recieve_queue
        #: object Object that we're proxying for
        self._proxy_for = proxy_for

    def reloder_proxy_listen(self):
        """
        Block on the recieve_queue. Once you get a message, proxy it to the item and then dump
        the response into the send_queue. If we get a KILL message, leave the loop.
        """

        while True:
            func_name, args, kwargs = self._recieve_queue.get()
            try:

                result = getattr(self._proxy_for, func_name)(*args, **kwargs)
                self._send_queue.put(result)
            # Catch any exception here and bubble it up (be as transparent as
            # possible)
            except Exception as e:  # pylint: disable=broad-except,invalid-name
                self._send_queue.put(e)
            if func_name == "stop":
                break

    def __getattr__(self, name):
        """
        Needed to proxy arbitrary method calls.
        """

        # Check if it's something we actually need to get
        if name in ('_send_queue', '_recieve_queue', '_proxy_for'):
            return super(ReloaderProxy, self).__getattr__(name)

        def wrapper(*args, **kwargs):
            self._send_queue.put((name, list(args), kwargs))
            result = self._recieve_queue.get()
            if isinstance(result, Exception):
                raise result
            return result
        return wrapper


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

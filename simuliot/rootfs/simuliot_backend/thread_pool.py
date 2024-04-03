import threading
import queue

class ThreadPool:
    def __init__(self, devices):
        self.devices = devices
        self.threads = []
        self.stop_flag = threading.Event()

    def start(self):
        for device in self.devices:
            thread = threading.Thread(target=self._start, args=(device,))
            thread.start()
            self.threads.append(thread)

    def _start(self, device):
        while not self.stop_flag.is_set():
            try:
                device.publish()
            except queue.Empty:
                continue

    def stop(self):
        self.stop_flag.set()
        for thread in self.threads:
            thread.join()
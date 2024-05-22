import threading
import queue
from time import sleep
import simuliot

class ThreadPool:
    def __init__(self, devices):
        self.devices = devices
        self.threads = []
        self.stop_flag = threading.Event()
        self.pause_flag = threading.Event()

    def start(self):
        for device in self.devices:
            thread = threading.Thread(target=self._start, args=(device,))
            thread.start()
            self.threads.append(thread)

    def _start(self, device):
        while not self.stop_flag.is_set():
            try:
                if self.pause_flag.is_set():
                    continue
                device.publish()
                sleep(5)
                # Commented out block
                # match (device.type):
                #     case 'Switch':
                #         sleep(5)
                #     case 'Hub':
                #         device.publish()
                #         sleep(5)
                #     case 'Thermometer':
                #         device.publish()
                #         sleep(5)
                #     case 'US_Sensor':
                #         sleep_for = device.sleep()
                #         device.publish()
                #         sleep(sleep_for)
                #     case 'Volume_Sensor':
                #         device.publish()
                #         sleep(5)
                #     case 'Thermo_Switch':
                #         device.publish()
                #         sleep(5)
                #     case 'Switch_Config':
                #         sleep(5)
                #     case default:
                #         device.publish()
                #         sleep(5)
                # if device.type != 'Switch':
                #     device.publish()
                #     sleep(5)
            except queue.Empty:
                continue

    def pause(self):
        self.pause_flag.set()

    def resume(self):
        self.pause_flag.clear()

    def stop(self):
        self.stop_flag.set()
        for thread in self.threads:
            thread.join()
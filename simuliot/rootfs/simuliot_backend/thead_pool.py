from threading import Thread
import simuliot, os

def init_thead(devicesCurrentSession):
    simuliot.logger.info('Initializing thread pool')
    device_thread = Thread(target = simuliot.start, args = (devicesCurrentSession,))
    device_thread.start()
    return device_thread

def fork_process(devicesCurrentSession):
    simuliot.logger.info('Forking process')
    device_thread_pid = os.fork()
    if device_thread_pid == 0:
        init_thead(devicesCurrentSession)
    return device_thread_pid
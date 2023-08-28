from random import randint, uniform
import uuid

# This class simulates all contant and non contact temperature probes. This is measured against the absolute zero (0 Kelvin) which is -273.15 degrees Celsius. The maximum temperature that can be recorded by this device is 300 degrees Celsius.
# For non contact sensors (ie. sensors that use infrared or metal devices) the temperature range is -20 to 60 degrees Celsius.

class tempDevice:
    def __init__(self, dbConn, deviceID):
        self.dbConn = dbConn
        self.deviceID = deviceID

    def contactProbe(self):
        return round(uniform(-273.15, 300), 2)
    
    def nonContactProbe(self):
        return round(uniform(-20, 60), 2)
    
    def getDeviceID(self):
        return str(uuid.uuid4())
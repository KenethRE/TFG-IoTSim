from django.db import models
from django.core import serializers

# Create your models here.
class Plano(models.Model):
    Upload_Map = models.ImageField(upload_to='images/maps/')

    class Meta:
        app_label = 'starthere'

class DeviceManager(models.Manager):
    def mapTypeToIcon(self, Type):
        match Type:
            case 'Thermometer':
                return 'thermometer'
            case 'Water_Flow':
                return 'water'
            case 'Air_Flow':
                return 'air'
            case 'US_Sensor':
                return 'sensors'
            case 'Switch':
                return 'switch'
            case 'Hub':
                return 'router'
            case 'Switch_Config':
                return 'tune'
            case 'Thermo_Config':
                return 'nest_thermostat'
            case 'Thermo_Switch':
                return 'switch'
            case 'Volume_Sensor':
                return 'brand_awareness'

    def create_device(self, DeviceID, Type, Description, Manufacturer):
        device = self.create(DeviceID=DeviceID, Type=self.mapTypeToIcon(Type), Description=Description, Manufacturer=Manufacturer)
        return device
    def create_session_device(self, DeviceID, Type, Location):
        device = self.create(DeviceID=DeviceID, Type=Type, Location=Location)
        return device

class Devices(models.Model):
    DeviceID = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    Description = models.CharField(max_length=50)
    Manufacturer = models.CharField(max_length=50)
    Value = models.CharField(max_length=50, default='0')
    Location = models.CharField(max_length=50, default='0')
    objects = DeviceManager()

    def printDevice(self):
        deviceString = {
            "DeviceID": self.DeviceID,
            "Type": self.Type,
            "Description": self.Description,
            "Manufacturer": self.Manufacturer,
            "Value": self.Value,
            "Location": self.Location
        }
        return deviceString

    class Meta:
        app_label = 'starthere'
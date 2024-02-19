from django.db import models

# Create your models here.
class Plano(models.Model):
    Upload_Map = models.ImageField(upload_to='images/maps/')

    class Meta:
        app_label = 'starthere'

class DeviceManager(models.Manager):
    def create_device(self, DeviceID, Type, Description, Manufacturer):
        device = self.create(DeviceID=DeviceID, Type=Type, Description=Description, Manufacturer=Manufacturer)
        return device

class Devices(models.Model):
    DeviceID = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    Description = models.CharField(max_length=50)
    Manufacturer = models.CharField(max_length=50)

    objects = DeviceManager()

    class Meta:
        app_label = 'starthere'
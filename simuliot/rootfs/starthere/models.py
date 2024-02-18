from django.db import models

# Create your models here.
class Plano(models.Model):
    Nombre_Imagen = models.CharField(max_length=50)
    Subir_Plano = models.ImageField(upload_to='images/maps/')

    class Meta:
        app_label = 'starthere'

class Devices(models.Model):
    Type = models.CharField(max_length=50)
    Description = models.CharField(max_length=50)
    Manufacturer = models.CharField(max_length=50)

    class Meta:
        app_label = 'starhere'
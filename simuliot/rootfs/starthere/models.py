from django.db import models

# Create your models here.
class Plano(models.Model):
    Nombre_Imagen = models.CharField(max_length=50)
    Subir_Plano = models.ImageField(upload_to='images/')
    
    class Meta:
        app_label = 'starthere'
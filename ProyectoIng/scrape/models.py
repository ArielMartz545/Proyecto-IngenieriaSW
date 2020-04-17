from django.db import models

# Create your models here.
# exchange
# Unidad-Tipo de Moneda, Intercambio-Valor de la moneda en lempiras
class Exchange(models.Model):
    unit= models.CharField(max_length=20)
    exchange= models.FloatField()
    sign= models.CharField(max_length=4, null= True, blank= True)

    def __str__(self):
        return self.unit

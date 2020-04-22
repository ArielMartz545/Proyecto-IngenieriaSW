from django.db import models

# Create your models here.
# exchange
# Unidad-Tipo de Moneda, Intercambio-Valor de la moneda en lempiras
class Exchange(models.Model):
    unit= models.CharField(max_length=20, verbose_name='Moneda')
    exchange= models.FloatField( verbose_name='Intercambio a Lempiras')
    sign= models.CharField(max_length=4, null= True, blank= True, verbose_name='Signo')

    class Meta():
        verbose_name= "Intercambio Lempiras"
        verbose_name_plural= "Intercambios de Moneda"

    def __str__(self):
        return self.unit

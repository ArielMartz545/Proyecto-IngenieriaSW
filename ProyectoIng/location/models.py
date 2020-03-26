from django.db import models

# Create your models here.
"""Clase Ubicacion"""
class Location(models.Model):
    direction = models.CharField(primary_key=True, max_length=50, default="Ninguna")
    correlative_direction= models.ForeignKey("self",on_delete=models.CASCADE, default="Ninguna", blank=True, null=True)

    def __str__(self):
        if  self.correlative_direction:
            return self.direction + ", " + self.correlative_direction.direction
        return self.direction
    
    class Meta():
        verbose_name= "Ubicación"
        verbose_name_plural= "Ubicaciones"
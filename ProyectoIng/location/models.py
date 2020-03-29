from django.db import models

# Create your models here.
"""Clase Ubicacion"""
class Location(models.Model):
    direction = models.CharField(max_length=50)
    correlative_direction= models.ForeignKey("Location",on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if  self.correlative_direction:
            return self.direction + ", " + self.correlative_direction.direction
        return self.direction
    
    class Meta():
        verbose_name= "Ubicación"
        verbose_name_plural= "Ubicaciones"
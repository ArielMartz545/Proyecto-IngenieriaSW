from django.db import models
import uuid

def images_directory_path(instance, filename):
    return '/'.join(['images', str(uuid.uuid4().hex + "."+filename.split(".")[-1])])

# Create your models here.
"""Clase imagenes:
Atributo: [Direccion de la imagen]"""
class Image(models.Model):
    img_route= models.ImageField(upload_to=images_directory_path, verbose_name="Ruta de la Imagen")

    class Meta():
        verbose_name= "Imagen"
        verbose_name_plural= "Imagenes"










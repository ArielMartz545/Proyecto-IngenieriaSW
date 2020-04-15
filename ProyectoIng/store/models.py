from django.db import models
from location.models import Location
from account.models import Account
from images.models import Image
# Create your models here.
"""Clase Tienda, 
Atributos: [Nombre, descripcion, ubicacion de tienda]"""

class Store(models.Model):
    store_name= models.CharField(max_length=100,null=False,blank=False)
    store_description= models.TextField(null=False,blank=False)
    store_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    store_images= models.ManyToManyField(Image, related_name="get_images_store")
    #Booleano para saber si la tienda esta activa o no (Borrada o no)
    active= models.BooleanField(default=True)

    def __str__(self):
        return self.store_name

    class Meta():
        verbose_name= "Tienda"
        verbose_name_plural= "Tiendas"

    def user_is_owner(self, user):
        users = UsersXStore.objects.values('user').get(store = self)
        for u in users.values():
            if user.id == u:
                return True
        return False

class UsersXStore(models.Model):
    store= models.ForeignKey(Store, on_delete=models.CASCADE)
    user= models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.store.store_name+", "+self.user.email
    
    class Meta():
        verbose_name= "Usuario por Tienda"
        verbose_name_plural= "Usuarios por Tiendas"
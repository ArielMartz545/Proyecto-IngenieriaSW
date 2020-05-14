from django.db import models
from account.models import Account
from store.models import Store
# Create your models here.
class Favorites(models.Model):
    id_user= models.ForeignKey(Account, on_delete=models.CASCADE)
    id_favorite_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = "favoritos" )
    
    class Meta():
        verbose_name= "Favorito"
        verbose_name_plural= "Favoritos"

    def __str__(self):
        return "Usuario: " + self.id_user.first_name +" Favorito: " + self.id_favorite_user.first_name


class Favorites_Store(models.Model):
    id_user= models.ForeignKey(Account, on_delete=models.CASCADE)
    id_favorite_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name = "favoritos_tiendas" )
    
    class Meta():
        verbose_name= "Tienda Favorito"
        verbose_name_plural= "Tiendas Favoritos"

    def __str__(self):
        return "Usuario: " + self.id_user.first_name +" Favorito: " + self.id_favorite_store.store_name
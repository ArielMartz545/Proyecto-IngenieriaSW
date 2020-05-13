from django.db import models
from account.models import Account
from store.models import Store
from ad.models import Ad, Category, PriceRange, Currency
from location.models import Location

# Create your models here.
class Search(models.Model):
    #Usuario que busca
    id_user = models.ForeignKey(Account, on_delete=models.CASCADE, default = None, blank=True, null=True)
    #Lugar en el que busca
    id_location= models.ForeignKey(Location, on_delete= models.CASCADE, default = None, blank=True, null=True)
    #Categoria en la que busca
    id_category= models.ForeignKey(Category, on_delete= models.CASCADE, default = None, blank=True, null=True)
    #Moneda en la que busca
    id_currency= models.ForeignKey(Currency, on_delete= models.CASCADE, default = None, blank=True, null=True)
    #Rango de precio en el que busca
    #Usar el set_id_price_range para asignar correctamente
    id_price_range = models.ForeignKey(PriceRange, on_delete= models.CASCADE, default = None, blank=True, null=True)
    #Palabras para busqueda del usuario
    query_search = models.TextField()
    #Puntuacion minima que se uso para la busqueda
    min_rating = models.IntegerField(default = None, blank=True, null=True)
    #Es busqueda de anuncios
    ad_search = models.BooleanField(default=False)
    #Es busqueda de usuarios
    user_search = models.BooleanField(default=False)
    #Es busqueda de tiendas
    store_search = models.BooleanField(default=False)
    #Es un rango de precios personalizado por el usuario
    custon_price_range = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.pk)+" "+ self.query_search

    def set_id_price_range(self, min, max, currency):
        if currency is None:
            self.custom_price_range = True
        else:
            price_range = PriceRange.objects.get(min_price = min, max_price = max, currency = currency)
            if price_range:
                self.id_price_range = price_range
                self.custom_price_range = True

    class Meta():
        verbose_name= "Busqueda"
        verbose_name_plural= "Busquedas"
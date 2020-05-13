from django.db import models
from account.models import Account
from store.models import Store
from location.models import Location
from images.models import Image
from scrape.models import Exchange
from rating.models import Rating
from django.db.models import Value, Case, When, F, OuterRef, Subquery, Avg


from django.forms.models import model_to_dict

# Create your models here.
class Disable_ads(models.Model):
    time_to = models.IntegerField(verbose_name="Dias Para desabilitar Anuncios")

    class Meta():
        verbose_name = "Dias para desabilitar anuncios"
    
    def __str__(self):
        return "Dias para desailitar, recomendado 15"
    

"""Clase Categoria
Atributos: [Nombre, descripcion e icono de la categoria]"""
class Category(models.Model):
    category_name=models.CharField(max_length=100,blank=False,null=False)
    category_description= models.TextField(null=False, blank=False)
    category_icon_class= models.CharField(max_length=100,null=False, blank=False)

    def __str__(self):
        return self.category_name
    
    class Meta():
        verbose_name= "Categoría"
        verbose_name_plural= "Categorías"

"""Clase Tipo Anuncio
Atributo: TIpoAnuncio"""
class AdKind(models.Model):
    ad_kind= models.CharField(max_length=20)

    def __str__(self):
        return self.ad_kind
    
    class Meta():
        verbose_name= "Tipo de Anuncio"
        verbose_name_plural= "Tipos de Anuncio"

"""Clase Unidad,
Atributo: Unidad"""
class Unit(models.Model):
    unit_type= models.CharField(max_length=10, default="Unidad")

    def __str__(self):
        return self.unit_type
    
    class Meta():
        verbose_name= "Unidad"
        verbose_name_plural= "Unidades"


"""Clase Moneda
Atributos: [Nombre de la moneda, cambio]"""
class Currency(models.Model):
    currency_name= models.CharField(max_length=100,blank=False,null=False)
    currency_sign = models.CharField(max_length=5,blank=False,null=False)

    def __str__(self):
        return self.currency_name

    class Meta():
        verbose_name= "Moneda"
        verbose_name_plural= "Monedas"

"""Clase Rango de precio,
Atributos: [Precio minimo y maximo, ID moneda]"""
class PriceRange(models.Model):
    min_price = models.FloatField(blank=False,null=False)
    max_price = models.FloatField(blank=False,null=False)
    currency = models.ForeignKey(Currency, on_delete= models.CASCADE)

    def __str__(self):
        return self.currency.currency_sign+str(self.min_price)+'-'+str(self.max_price)

    class Meta():
        verbose_name= "Rango de Precio"
        verbose_name_plural= "Rangos de Precio"


class AdSet(models.QuerySet):
    def publisher_rating(self):
        return self.annotate(
            publisher_rating=Case(
                #Obtener promedio de usuario
                When(id_store__isnull = True, then = 
                    Subquery(Rating.objects.filter(evaluated_user=OuterRef('id_user'))
                    .annotate(rating=Avg('points'))
                    .values('rating')[:1])
                ),
                #Obtener promedio de tienda
                When(id_store__isnull = False, then = 
                    Subquery(Rating.objects.filter(evaluated_user=OuterRef('id_store'))
                    .annotate(rating=Avg('points'))
                    .values('rating')[:1])
                ),
                output_field=models.FloatField(),
            ),
        )


"""Clase Anuncio:
Atributos: [ID Usuario, ID Tienda, ID ubicacion, ID tipo anuncio, ID Categoria, ID Unidad, 
            nombre y descripcion del anuncio, precio del anuncio y fecha de creacion]"""
class Ad(models.Model):
    id_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_store = models.ForeignKey(Store, on_delete= models.CASCADE,default=None, blank=True, null=True)
    id_location= models.ForeignKey(Location, on_delete= models.CASCADE)
    id_ad_kind= models.ForeignKey(AdKind, on_delete= models.CASCADE)
    id_category= models.ForeignKey(Category, on_delete= models.CASCADE)
    id_unit= models.ForeignKey(Unit, on_delete= models.CASCADE, default = None, blank=True, null=True)
    id_currency= models.ForeignKey(Currency, on_delete= models.CASCADE)
    ad_name= models.CharField(max_length=100)
    ad_description= models.TextField()
    price= models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    ad_images= models.ManyToManyField(Image, related_name="get_images_ad")
    active= models.BooleanField(default=True)
    reason = models.CharField(max_length=20, null=True, blank=True) #Razones: [sold, user, automatic]
    def __str__(self):
        return self.ad_name

    def exchange(self):
        dolar_value_object=Exchange.objects.get(pk=1)
        dolar_value_dict= model_to_dict(dolar_value_object)
        if  self.id_currency.pk == 1:
            return self.price / dolar_value_dict['exchange']
        else:
            return self.price * dolar_value_dict['exchange']

    def exchange_currency(self):
        if  self.id_currency.pk == 1:
            return Currency.objects.get(pk = 2)
        else:
            return Currency.objects.get(pk = 1)

    objects = AdSet.as_manager()

    class Meta():
        verbose_name= "Anuncio"
        verbose_name_plural= "Anuncios"




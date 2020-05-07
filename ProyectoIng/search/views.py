from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.db.models import Value
from django.db.models.functions import Concat
from ad.models import Ad, Category, PriceRange, Currency, AdKind
from location.models import Location
from account.models import Account
from store.models import Store
from images.models import Image

class SearchView(ListView):
    template_name="search/search.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        context['ad_kinds'] = AdKind.objects.all()
        # Fin Sidebar Context
        q = self.request.GET.get("search_q")
        if q is None:
            q=""
        currency = self.request.GET.get("search_currency")
        if currency is None:
            currency=1
        try:
            min_price = float(self.request.GET.get("search_min"))
        except:
            min_price = 0
        try:
            max_price = float(self.request.GET.get("search_max"))
        except:
            max_price = 0
        try:
            c = int(self.request.GET.get("search_c"))
        except:
            c = 0
        try:
            l = int(self.request.GET.get("search_l"))
        except:
            l = 0
        try:
            category_name = Category.objects.get(pk=c).category_name
        except:
            category_name = "Todas las categorías"
        try:
            location_name = str(Location.objects.get(pk=l))
        except:
            location_name = "Todo lugar"
        if c == -1:
            context['ad_search'] = False
            context['user_search'] = True
            context['store_search'] = False
        elif c == -2:
            context['ad_search'] = False
            context['user_search'] = False
            context['store_search'] = True
        else:
            context['ad_search'] = True
            context['user_search'] = False
            context['store_search'] = False
        context['search_q'] = q
        context['search_currency'] = currency
        context['search_min'] = min_price
        context['search_max'] = max_price
        context['search_c'] = c
        context['search_l'] = l
        context['search_category_name'] = category_name
        context['search_location_name'] = location_name
        context['default_image'] = Image.objects.get(pk=1)
        return context

    def get_queryset(self):
        q = self.request.GET.get("search_q")
        if q is None:
            q=""
        try:
            min_price = float(self.request.GET.get("search_min"))
        except:
            min_price = 0
        try:
            max_price = float(self.request.GET.get("search_max"))
        except:
            max_price = 0
        try:
            c = int(self.request.GET.get("search_c"))
        except:
            c = 0
        try:
            l = int(self.request.GET.get("search_l"))
        except:
            l = 0
        if c == -1:
            #Busqueda de usuarios
            queryset = Account.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
            queryset = queryset.filter(full_name__icontains=q) | queryset.filter(email__icontains=q)
            return queryset
        elif c == -2:
            #Busqueda de tiendas
            queryset = Store.objects.filter(active=True)
            queryset = queryset.filter(store_name__icontains=q) | queryset.filter(store_description__icontains=q)
            try:
                location = Location.objects.get(pk=l)
            except:
                location = None
            #Filtro de lugar
            if location is not None:
                queryset = queryset.filter(store_location__pk=l) | queryset.filter(store_location__correlative_direction__pk=l)
            #queryset = queryset.order_by('-date_created')
            return queryset
        else:
            #Busqueda de anuncios
            #Validacion de minimo y maximo
            #Si solo se selecciono precio minimo, el precio maximo viene con valor 0
            #Si solo se selecciono precio maximo, el precio minimo viene con valor 0
            #Si no se selecciono minimo ni maximo, ambos vienen con valor 0
            if  (min_price > max_price and max_price != 0):
                temp = max_price
                max_price = min_price
                min_price = temp
            #Filtro de precios
            queryset = Ad.objects.filter(price__gte=(min_price))
            if (max_price != 0):
                #Se selecciono un precio maximo
                queryset = queryset.filter(price__lte=(max_price))
            #Validacion de categorias
            try:
                category = Category.objects.get(pk=c)
            except:
                category = None
            #Filtro de categorias
            if category is not None:
                queryset = queryset.filter(id_category__pk=c)
            #Validacion de lugar
            try:
                location = Location.objects.get(pk=l)
            except:
                location = None
            #Filtro de lugar
            if location is not None:
                queryset = queryset.filter(id_location__pk=l) | queryset.filter(id_location__correlative_direction__pk=l)
            #Filtro de nombre o descripcion
            queryset = queryset.filter(ad_name__icontains=q) | queryset.filter(ad_description__icontains=q)
            queryset = queryset.filter(active=True).order_by('-date_created')
            return queryset

from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from ad.models import Ad, Category, PriceRange
from location.models import Location

class SearchView(ListView):
    model = Ad
    template_name="search/search.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        # Fin Sidebar Context
        q = self.request.GET.get("q")
        if q is None:
            q=""
        try:
            min_price = float(self.request.GET.get("min"))
        except:
            min_price = 0
        try:
            max_price = float(self.request.GET.get("max"))
        except:
            max_price = 0
        try:
            c = int(self.request.GET.get("c"))
        except:
            c = 0
        try:
            l = int(self.request.GET.get("l"))
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
        context['q'] = q
        context['min'] = min_price
        context['max'] = max_price
        context['c'] = c
        context['l'] = l
        context['category_name'] = category_name
        context['location_name'] = location_name
        return context

    def get_queryset(self):
        q = self.request.GET.get("q")
        if q is None:
            q=""
        try:
            min_price = float(self.request.GET.get("min"))
        except:
            min_price = 0
        try:
            max_price = float(self.request.GET.get("max"))
        except:
            max_price = 0
        try:
            c = int(self.request.GET.get("c"))
        except:
            c = 0
        try:
            l = int(self.request.GET.get("l"))
        except:
            l = 0
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
        queryset = queryset.filter(ad_name__contains=q) | queryset.filter(ad_description__contains=q)
        queryset = queryset.filter(active=True).order_by('-date_created')
        return queryset

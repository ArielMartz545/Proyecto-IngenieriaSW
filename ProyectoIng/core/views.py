from django.shortcuts import render
from django.views.generic.base import TemplateView
from ad.models import Category, PriceRange, Currency
from location.models import Location
from django.views.generic.detail import DetailView
from ad.models import Category,Ad
from scrape.models import Exchange
from django_globals import globals
from django.forms.models import model_to_dict
# Create your views here.

class main_page(TemplateView):
    template_name= "core/home.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        #Global Var
        #globals.request.session['dolar_exchange']=  model_to_dict(Exchange.objects.get(pk=1))
        
        return context


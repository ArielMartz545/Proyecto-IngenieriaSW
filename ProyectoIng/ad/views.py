from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Ad, Category, PriceRange
from location.models import Location
from account.models import Account
from images.models import Image


class ShowAdsListView(ListView):
    model= Ad
    template_name="ad_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["ads_data"]= Ad.objects.prefetch_related().order_by('-date_created')
        return context
#id_user ,id_store ,id_location,id_ad_kind,id_category,id_unit,ad_name,ad_description,price,date_created

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'ad/category_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products']= Ad.objects.all().order_by('-date_created')
        return context

class AdDetailView(DetailView):
    model = Ad 
    template_name = 'ad/ad_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['ads'] = Ad.objects.all().order_by('-date_created')
        return context
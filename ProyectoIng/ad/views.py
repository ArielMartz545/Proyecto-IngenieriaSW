from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import Ad, Category, PriceRange
from location.models import Location
from account.models import Account
from images.models import Image
from ad.forms import AdCreateForm,AdImageForm
from django.urls import reverse_lazy


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
        context['ads'] = Ad.objects.all().order_by('-date_created')
        return context



def AdCreate(request):
    model = Ad
    if  request.method == "POST" :
        ad_form= AdCreateForm(request.POST)
        img_form= AdImageForm(request.POST,request.FILES )
        print("img es "+ str(img_form.is_valid()))
        print(img_form)
        if ad_form.is_valid() and img_form.is_valid():
            img= img_form.save()
            ad= ad_form.save(False)
            ad.id_user = request.user
            ad= ad_form.save()
            ad.ad_images.add(img)#Esta debe ser una instancia de la tabla transaccional
            ad.save()
            print("Almacenado")
            return render(request,'ad/ad_list.html')
    else:
        ad_form=AdCreateForm()
        img_form=AdImageForm()

    return render(request,'ad/ad_create.html',{'Ad_form': ad_form,'img_form':img_form})
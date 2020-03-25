from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import Ad, Category, PriceRange
from location.models import Location
from account.models import Account
from images.models import Image
from ad.forms import AdCreateForm, AdImageForm
from django.urls import reverse_lazy, reverse
from django.forms import modelformset_factory


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

    ad_form=AdCreateForm()
    img_forms= modelformset_factory(Image, fields=("img_route",), extra=3,)

    if  request.method == "POST" :
        safe_form= AdImageForm()
        ad_form= AdCreateForm(request.POST)
        images_formset= img_forms(request.POST or None, request.FILES or None)
        
        if ad_form.is_valid() and images_formset.is_valid():

            ad= ad_form.save(False)
            ad.id_user = request.user
            ad= ad_form.save()

            for img in images_formset:
                img.cleaned_data['img_route']
                safe_img = img.save()
                ad.ad_images.add( safe_img )
                
            
            ad.save(False)
            return HttpResponseRedirect(reverse('my_products'))
    
    formset= img_forms(queryset = Image.objects.none())   
        

    return render(request,'ad/ad_create.html',{'Ad_form': ad_form,'formset':formset})

def AdCreate2(request):
    model = Ad

    ad_form=AdCreateForm()
    if  request.method == "POST" :
        safe_form= AdImageForm()
        ad_form= AdCreateForm(request.POST)
        
        if ad_form.is_valid():

            ad= ad_form.save(False)
            ad.id_user = request.user
            ad= ad_form.save()

            for file in request.FILES.getlist('images'):
                instance = Image(img_route=file)
                instance.save()
                ad.ad_images.add( instance )

            ad.save(False)
            return HttpResponseRedirect(reverse('my_products'))

    return render(request,'ad/ad_create2.html',{'Ad_form': ad_form})
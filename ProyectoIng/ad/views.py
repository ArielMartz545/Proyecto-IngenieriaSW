from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Ad, Category, PriceRange, AdKind, Unit, Currency
from location.models import Location
from account.models import Account
from images.models import Image
from ad.forms import AdCreateForm, AdUpdateForm, AdDeleteForm
from django.urls import reverse_lazy, reverse
from django.forms import modelformset_factory
from favorites.models import Favorites
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import re #Libreria para expresiones regulares

class UserAds(ListView):
    model= Ad
    template_name="ad/user_ad_list.html"
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        # Fin Sidebar Context
        uid = self.kwargs['uid']
        try:
            user = Account.objects.get(pk=self.kwargs['uid'])
        except:
            user = self.request.user
        context['user_name'] = user.get_full_name
        context['user_pk'] = user.pk
        return context
    def get_queryset(self):
        uid = self.kwargs['uid']
        try:
            user = Account.objects.get(pk=uid)
        except:
            user = self.request.user
        queryset = Ad.objects.filter(id_user__id=user.id, id_store__id=None)
        queryset = queryset.filter(active=True).order_by('-date_created')
        return queryset

class CategoryAds(ListView):
    model= Ad
    template_name="ad/category_ad_list.html"
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        # Fin Sidebar Context
        c = self.kwargs['cid']
        try:
            category = Category.objects.get(pk=c)
            context['category_name'] = category.category_name
            context['c'] = c
        except:
            context['category_name'] = "Todas las categorías"
            context['c'] = 0
        return context
    def get_queryset(self):
        cid = self.kwargs['cid']
        try:
            category = Category.objects.get(pk=cid)
            queryset = Ad.objects.filter(id_category__id=category.id)
        except:
            queryset = Ad.objects.all()
        queryset = queryset.filter(active=True).order_by('-date_created')
        return queryset

class AdDetailView(DetailView):
    model = Ad 
    template_name = 'ad/ad_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        # Fin Sidebar Context
        return context

@method_decorator(login_required, name='dispatch')
class CreateAd(CreateView):
    model = Ad
    form_class=AdCreateForm
    template_name= 'ad/ad_create.html' #Template al que envia el formulario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        # Fin Sidebar Context
        context['all_locations'] = Location.objects.all().order_by('direction')
        context['ad_kinds'] = AdKind.objects.all()
        context['units'] = Unit.objects.all()
        context['currencies'] = Currency.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = AdCreateForm(request.POST)
        if form.is_valid():
            ad= form.save(False)
            ad.id_user = request.user
            ad= form.save()
            for file in request.FILES.getlist('images'):
                instance = Image(img_route=file)
                instance.save()
                ad.ad_images.add( instance )
            if len(request.FILES.getlist('images'))==0:
                instance = Image.objects.get(pk=1)
                ad.ad_images.add( instance )
            ad.save(False)
            favs = Favorites.objects.all().filter(id_favorite_user = request.user)
            emails = []
            num = ad.id
            for fav in favs:
                emails.append(fav.id_user.email)
            html_message='<h1><a href=http://127.0.0.1:8000/ads/'+str(num)+'>Click</a></h1>'
            send_mail('Anuncio nuevo', 'Anuncio de tus favoritos', settings.EMAIL_HOST_USER,emails,html_message=html_message,fail_silently=False)
            return HttpResponseRedirect(reverse_lazy('products_user',kwargs={'uid':self.request.user.pk})+'?createdAd=success')
        return HttpResponseRedirect(reverse_lazy('ad_create')+'?createdAd=error')


@method_decorator(login_required, name='dispatch')
class AdDelete(UpdateView):
    model = Ad
    form_class= AdDeleteForm
    template_name = 'ad/ad_delete.html'
    context_object_name = 'Ad'
    
    def post(self, request,pk, *args, **kwargs):
        form =AdDeleteForm(request.POST)
        ad_object_data = self.object = self.get_object()
        if form.is_valid():
            ad= form.save(commit=False)
            ad= ad_object_data
            ad.active= False
            ad.save(False)
        ad.save()
        return HttpResponseRedirect(reverse_lazy('products_user',kwargs={'uid':self.request.user})+'?deleted')
 
        

@method_decorator(login_required, name='dispatch')
class AdUpdate(UpdateView):
    model = Ad
    form_class= AdUpdateForm
    template_name = 'ad/ad_update.html'
    context_object_name = 'Ad'

    def post(self, request,pk, *args, **kwargs):
        form =AdUpdateForm(request.POST)
        ad_object_data = self.object = self.get_object()

        if form.is_valid():
            ad= form.save(commit=False)
            ad.id_user = request.user
            ad.pk= ad_object_data.pk
            ad.id_store = ad_object_data.id_store
            ad.date_created = ad_object_data.date_created
            ad.save(False)
            if request.FILES.getlist('images'):
                ad.ad_images.clear()

            for file in request.FILES.getlist('images'):
                    instance = Image(img_route=file)
                    instance.save()
                    ad.ad_images.add(instance)
            ad.save()
        elif not form.is_valid and ad_object_data.id_store:
            return HttpResponseRedirect(reverse_lazy('store_detail',kwargs={'pk': ad_object_data.id_store.pk})+'?updatedAd=error')
        else:
            return HttpResponseRedirect(reverse_lazy('products_user',kwargs={'uid': self.request.user.id})+'?updatedAd=error')
        """ El siguiente bloque de codigo tiene varias funcionalidades:
        1. En el TRY queremos hacer que retornemos al usuario a la pagina de anuncios generales de cada categoria luego de editar el anuncio,
            asi el usuario no tiene que regresar a la pagina de anuncios, por ejemplo regresar a la categoria Educacion.
        2. En el primer IF del except queremos que si actualizamos un anuncio desde la tienda, entonces seamos regresado a la tienda
        3. Si editamos un anuncio desde la lista de anuncios de un usuario comun, entonces te redirecciona a la misma pagina de la lista de 
            anuncios de ese usuario comun."""
        try: 
            #Obtenemos el request que se manda desde products_category, ejemplo: '/ads/category/1'
            temp = re.findall(r'\d+', request.GET['next']) 
            #con REGEX obtenemos el ID que se envia en el request
            res = list(map(int, temp)) 
            return HttpResponseRedirect(reverse_lazy('products_category',kwargs={'cid': res[0]})+'?updatedAd=success')
        except:
            if ad_object_data.id_store:
                return HttpResponseRedirect(reverse_lazy('store_detail',kwargs={'pk': ad_object_data.id_store.pk})+'?updatedAd=success')
            else:
                return HttpResponseRedirect(reverse_lazy('products_user',kwargs={'uid':self.request.user.id})+'?updatedAd=success')
 
        
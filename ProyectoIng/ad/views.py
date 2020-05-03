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
from store.models import Store, UsersXStore
from store.views import owners
from ad.forms import AdCreateForm, AdUpdateForm, AdDeleteForm
from django.urls import reverse_lazy, reverse
from django.forms import modelformset_factory
from favorites.models import Favorites
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import re #Libreria para expresiones regulares

class StoreAds(ListView):
    model= Ad
    template_name="ad/store_ad_list.html"
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        context['owners'] = owners(self.kwargs['sid'])
        # Fin Sidebar Context
        sid = self.kwargs['sid']
        try:
            store = Store.objects.get(pk=sid)
            context['valid_store'] = True
        except:
            context['valid_store'] = False
        if context['valid_store']:
            context['store_name'] = store.store_name
            context['store_pk'] = store.pk
        return context
    def get_queryset(self):
        sid = self.kwargs['sid']
        queryset = Ad.objects.filter(id_store__id=sid)
        queryset = queryset.filter(active=True).order_by('-date_created')
        return queryset

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
        context['ad_kinds'] = AdKind.objects.all()
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
        context['ad_kinds'] = AdKind.objects.all()
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

#Clase para crear un Anuncio 
@method_decorator(login_required, name='dispatch')
class CreateAd(CreateView):
    model = Ad
    form_class = AdCreateForm
    #Sobrecarga del metodo POST
    def post(self, request, *args, **kwargs):
        #Obteniendo la instancia del Formulario
        form = AdCreateForm(request.POST)
        #Si el formulario es valido se hace la creacion del anuncio, sino se hace un redireccionamiento por el error
        if form.is_valid():
            next_url = request.POST.get('next_url')
            ad = form.save(False)
            ad.id_user = request.user
            ad = form.save()
            #Verificando que el anuncio esta siendo creado desde una tienda, si es asi se agrega agrega el id de tienda al anuncio
            if request.POST.get('id_store') is not None:
                try:
                    id_store = request.POST.get('id_store')
                    #Verificando que la tienda exista
                    store = Store.objects.get(pk = id_store)
                    """ Verificando que el usuario que hizo la peticion es el administardor de la pagina, si no es asi hace redireccionamiento """
                    if not store.user_is_owner(request.user):
                        return HttpResponseRedirect(reverse_lazy('home'))
                    ad.id_store = store
                except:
                    return HttpResponseRedirect(reverse_lazy('home')) 
            ad.save()
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
            return HttpResponseRedirect(next_url+'?createdAd=success')
        return HttpResponseRedirect(next_url+'?createdAd=error')

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
            return HttpResponseRedirect(request.GET['next'] +'?updatedAd=success')
        except:
            if ad_object_data.id_store:
                return HttpResponseRedirect(reverse_lazy('store_detail',kwargs={'pk': ad_object_data.id_store.pk})+'?updatedAd=success')
            else:
                return HttpResponseRedirect(reverse_lazy('products_user',kwargs={'uid':self.request.user.id})+'?updatedAd=success')
 

#FUNCION QUE ELIMINA LOS ANUNCIOS ATRAVES DE LA VENTANA MODAL
def adDelete(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))
    #Obteniendo a donde seremos redireccionado para cada response
    next_url = request.POST.get('next_url')
    #Obteniendo el ID del anuncio
    id_ad = request.POST.get('id_ad')
    next_url = request.POST.get('next_url')
    """ Verificando que el anuncio exista """
    try:
        ad = Ad.objects.get(pk = id_ad) 
    except:
        #Redirecciona porque el anuncio no fue encontrado.
        return HttpResponseRedirect(next_url+'?AdError=AdNotFound')
    #Verificando que el anuncio no fue creado desde una tienda y quien hace la peticion no es el creador del anuncio
    if ad.id_store is None and ad.id_user != request.user:
        return HttpResponseRedirect(reverse_lazy('home'))
    #Verificando que el anuncio fue creado por una tienda
    elif ad.id_store is not None:
        store = Store.objects.get(pk = ad.id_store.pk)
        #Verificando que quien hace la peticion es owner de la tienda, sino manda al home
        if request.user.pk not in owners(ad.id_store.pk):
            return HttpResponseRedirect(reverse_lazy('home'))
    #Dado que cumple las condiciones de seguridad, procedemos a eliminar el anuncio
    if request.method == "POST":
        #Next_url es la direccion a la que seremos reenviado (Es donde se hizo la peticion)
        form = AdDeleteForm(request.POST, instance= ad)
        if form.is_valid():
            ad = form.save()
            ad.active = False
            #Obteniendo el valor del option button seleccionado en el modal.
            value = request.POST.get('delete')
            if (value == '0'):
                #El usuario selecciono que el anuncio fue vendido
                ad.reason = "sold"
            elif (value == '1'):
                #El usuario selecciono que lo elimino por otra razon distinta a venderlo.
                ad.reason = "user"
            ad.save(False)
            return HttpResponseRedirect(next_url+'?deletedAd=success')
    return HttpResponseRedirect(next_url+'?deleteAd=error')
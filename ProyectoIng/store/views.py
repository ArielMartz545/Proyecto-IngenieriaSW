from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from ad.models import Category, PriceRange, Currency
from location.models import Location
from store.models import Store
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from ad.models import Ad, AdKind, Unit, Currency
from images.models import Image
from .models import Store, UsersXStore
from .forms import StoreForm, StoreUpdateForm, StoreDeleteForm
from ad.forms import AdCreateForm
from django.http import  HttpResponseRedirect
from django.views import View
# Create your views here.

#Clase para crear una tienda
class CreateStore(CreateView): #Pass,Correo,Nombre,Apellido,Telefono,Direccion,FechaN
    model = Store
    form_class=StoreForm
    #Se sobrecarga el metodo post para poder agregar mas de un usuario a la tienda, asi como el usuario que la crea y las imgs
    def post(self, request, *args, **kwargs):
        #Obteniendo la instancia del formulario
        form = StoreForm(request.POST)
        #Si el formulario es valido se hace la creacion de la tienda, sino se hace un redireccionamiento por el error
        if form.is_valid():
            store = form.save()
            store.save()
            user_store = UsersXStore()
            user_store.user = request.user
            user_store.store = store
            user_store.save()
            store.save(False)
            return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.id})+'?added=success')
        return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.id})+'?added=error')
    
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.id}))

#Esta clase sirve para desplegar las tiendas asociadas a un usuarios
class UserStores(ListView):
    model= UsersXStore
    template_name="store/stores_list.html"
    #Numero de elementos por paginacion
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        # Fin Sidebar Context
        context['all_locations'] = Location.objects.all().order_by('direction')
        #Lo comentado entre comillas serviria si se desea permitir a otros usuarios ver las tiendas que poseen los demas usuarios
        """uid = self.kwargs['uid']"""
        user = self.request.user
        """try:
            user = Account.objects.get(pk=uid)
        except:
            user = self.request.user
        """
        context['user_name'] = user.get_full_name
        context['user_pk'] = user.pk
        return context
    def get_queryset(self):
        """uid = self.kwargs['uid']
        try:
            user = Account.objects.get(pk=uid)
        except:
            user = self.request.user
        """
        return UsersXStore.objects.prefetch_related('store').filter(user=self.request.user).order_by('-store__store_name')

#Esta clase sirve para ver la informacion detallada de una tienda
class StoreDetailView(DetailView):
    model = Store 
    template_name = 'store/stores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Obteniendo la tienda
        context['stores'] = Store.objects.all()
        #Obteniendo las divisas
        context['currencies'] = Currency.objects.all()
        #Obteniendo tipo de anuncios
        context['ad_kinds'] = AdKind.objects.all()
        #Obteniendo Unidades
        context['units'] = Unit.objects.all()
        #obteniendo Categoria de los anuncios
        context['categories'] = Category.objects.order_by('category_name')
        #Obtniendo las locaciones
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        #El siguiente diccionario contiene todos los usuarios que son administradores de la tienda
        users_dic = UsersXStore.objects.values('user').filter(store = kwargs['object'].pk)
        owners = [] #La lista nos servira para almacenar los ID que estan en el diccionario anterior
        for i in users_dic: owners.append(i['user'])
        #Se envia una lista que contiene el ID de los administradores de la tienda que servira para verificaciones en el template
        context['owners'] = owners
        #Consulta para obtener los anuncios realizados con la tienda
        queryset = Ad.objects.filter(id_store__id=kwargs['object'].pk)
        queryset = queryset.filter(active=True).order_by('-date_created')
        context['ads'] = queryset
        return context

class StoreUpdate(UpdateView):
    model = Store
    form_class = StoreUpdateForm
    template_name = 'store/store_update.html'

    def get_success_url(self):
        return reverse_lazy('store_detail',kwargs={'pk': self.object.id})+'?updated=success'

#Metodo hecho para poder actualizar los datos de una tienda desde el mismo template de detalle de tienda, hecho con un MODAL
def update_store(request, *args, **kwargs):
    #Obteniendo el id de la tienda
    id_store = request.POST.get('id_store')
    """ Se verifica que la tienda exista, 
        Si la tienda no existe store = None y se hace y redireccionamiento dado que la tienda no fue encontrada"""
    try:
        store = Store.objects.get(pk = id_store)
    except:
        return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.id})+'?error=storeNotFound')
    """ Verificando que el usuario que hizo la peticion es el administardor de la pagina, si no es asi hace redireccionamiento """
    if not store.user_is_owner(request.user):
        if request.user is None:
            return HttpResponseRedirect(reverse_lazy('login'))
        return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.id})+'?error=storeNotFound')
    #Solo solicitudes por metodo POST
    if request.method == "POST":
        form = StoreUpdateForm(request.POST, request.FILES or None, instance= store)
        if form.is_valid():
            store = form.save()
            #Obtener la imagen de perfil si subio una, sino asigna valor de False a user_img_route
            store_profile_img_route = request.FILES.get("store_profile_img", False)
            #Obtener la imagen de portada si subio una, sino asigna valor de False a cover_img_route
            store_cover_img_route = request.FILES.get("store_cover_img", False)
            #Solo si se subio imagen de perfil
            if  store_profile_img_route:
                if  store.store_profile_img.pk == 1:
                    store_profile_img = Image(img_route = store_profile_img_route)
                    store.store_profile_image = store_profile_img
                    store.store_profile_img.save()
                else:
                    store.store_profile_img.img_route = store_profile_img_route
                    store.store_profile_img.save()
            if  store_cover_img_route:
                if  store.store_cover_img.pk == 1:
                    store_cover_img = Image(img_route = store_cover_img_route)
                    store.store_cover_img = store_cover_img
                    store.store_cover_img.save()
                else:
                    store.store_cover_img.img_route = store_cover_img_route
                    store.store_cover_img.save()
            store.save(False)
            return HttpResponseRedirect(reverse_lazy('store_detail',kwargs={'pk': store.pk})+'?updated=success')
    return HttpResponseRedirect(reverse_lazy('store_detail',kwargs={'pk': store.pk})+'?updated=error')

class StoreDelete(UpdateView):
    model = Store
    form_class = StoreDeleteForm
    template_name = 'store/store_delete.html'
    context_object_name = 'Store'

    #Sobrecargando el metodo post
    def post(self, request, pk, *args, **kwargs):
        form = StoreDeleteForm(request.POST)
        store_object_data = self.object = self.get_object()
        if form.is_valid():
            store = form.save(commit=False)
            store = store_object_data
            #Se pasa el campo por defecto de Activo = True, a False. 
            store.active = False
            store.save(False)
        else:
            return HttpResponseRedirect(reverse_lazy('user_stores', kwargs={'uid': self.request.user})+'?deleted=error')
        store.save()
        return HttpResponseRedirect(reverse_lazy('user_stores', kwargs={'uid': self.request.user})+'?deleted=success')

""" Vista para crear anuncios desde una tienda"""
class CreateAdStore(CreateView):
    model = Ad
    form_class=AdCreateForm
    template_name= 'store/store_ad_create.html' #Template al que envia el formulario

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

    #sobrecarga del metodo post
    def post(self, request, *args, **kwargs):
        #Obteniendo el id de la tienda
        id_store = self.kwargs['pk']
        """ Se verifica que la tienda exista, 
            Si la tienda no existe store = None y se hace y redireccionamiento dado que la tienda no fue encontrada"""
        try:
            store = Store.objects.get(pk = id_store)
        except:
            return reverse_lazy('user_stores',kwargs={'pk': self.request.user.id})+'?error=storeNotFound'
        """ Verificando que el usuario que hizo la peticion es el administardor de la pagina, si no es asi hace redireccionamiento """
        if not store.user_is_owner(request.user):
            return reverse_lazy('user_stores',kwargs={'pk': self.request.user.id})+'?error=storeNotOwned'
        form = AdCreateForm(request.POST)
        if form.is_valid():
            ad= form.save(False)
            ad.id_user = request.user
            ad= form.save()
            ad.id_store = store 
            ad.save()
            for file in request.FILES.getlist('images'):
                instance = Image(img_route=file)
                instance.save()
                ad.ad_images.add( instance )
            if len(request.FILES.getlist('images'))==0:
                instance = Image.objects.get(pk=1)
                ad.ad_images.add( instance )
            ad.save(False)
            return HttpResponseRedirect(reverse_lazy('store_detail',kwargs={'pk': store.pk})+'?created=success')
        return HttpResponseRedirect(reverse_lazy('user_stores')+'?created=error')

#Metodo creado para crear anuncios desde una tienda
#def create_ad_store(request, *args, *args, **kwargs):
#Clase para crear un Anuncio asociado a una tienda
class CreateAdStore2(CreateView):
    model = Ad
    form_class = AdCreateForm
    #Sobrecarga del metodo POST
    def post(self, request, *args, **kwargs):
        id_store = request.POST.get('id_store')
        """ Se verifica que la tienda exista, 
            Si la tienda no existe store = None y se hace y redireccionamiento dado que la tienda no fue encontrada"""
        try:
            store = Store.objects.get(pk = id_store)
        except:
            return reverse_lazy('user_stores',kwargs={'pk': self.request.user.id})+'?error=storeNotFound'
        """ Verificando que el usuario que hizo la peticion es el administardor de la pagina, si no es asi hace redireccionamiento """
        if not store.user_is_owner(request.user):
            return reverse_lazy('user_stores',kwargs={'pk': self.request.user.id})+'?error=storeNotOwned'
        #Obteniendo la instancia del Formulario
        form = AdCreateForm(request.POST)
        #Si el formulario es valido se hace la creacion del anuncio, sino se hace un redireccionamiento por el error
        if form.is_valid():
            ad = form.save(False)
            ad.id_user = request.user
            ad = form.save()
            ad.id_store = store 
            ad.save()
            for file in request.FILES.getlist('images'):
                instance = Image(img_route=file)
                instance.save()
                ad.ad_images.add( instance )
            if len(request.FILES.getlist('images'))==0:
                instance = Image.objects.get(pk=1)
                ad.ad_images.add( instance )
            ad.save(False)
            return HttpResponseRedirect(reverse_lazy('store_detail',kwargs={'pk': store.pk})+'?created=success')
        return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.pk})+'?created=error')

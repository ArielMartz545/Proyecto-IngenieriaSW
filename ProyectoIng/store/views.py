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

class CreateStore(CreateView): #Pass,Correo,Nombre,Apellido,Telefono,Direccion,FechaN
    model = Store
    form_class=StoreForm

    def post(self, request, *args, **kwargs):
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save()
            store.save()
            user_store = UsersXStore()
            user_store.user = request.user
            user_store.store = store
            user_store.save()
            return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.id})+'?added')
        return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.id})+'?error')
    
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('user_stores',kwargs={'uid': request.user.id}))


class UserStores(ListView):
    model= UsersXStore
    template_name="store/stores_list.html"
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

class StoreDetailView(DetailView):
    model = Store 
    template_name = 'store/stores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stores'] = Store.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        return context

class StoreUpdate(UpdateView):
    model = Store
    form_class = StoreUpdateForm
    template_name = 'store/store_update.html'

    def get_success_url(self):
        return reverse_lazy('store_detail',kwargs={'pk': self.object.id})+'?updated=success'


class StoreDelete(UpdateView):
    model = Store
    form_class = StoreDeleteForm
    template_name = 'store/store_delete.html'
    context_object_name = 'Store'

    def post(self, request, pk, *args, **kwargs):
        form = StoreDeleteForm(request.POST)
        store_object_data = self.object = self.get_object()
        if form.is_valid():
            store = form.save(commit=False)
            store = store_object_data
            store.active = False
            store.save(False)
        store.save()
        return HttpResponseRedirect(reverse_lazy('user_stores', kwargs={'uid': self.request.user})+'?deleted=success')


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

    def post(self, request, *args, **kwargs):
        id_store = self.kwargs['pk']
        try:
            store = Store.objects.get(pk = id_store)
        except:
            return reverse_lazy('user_stores',kwargs={'pk': self.request.user.id})+'?error=storeNotFound'
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
            print(store)
            return HttpResponseRedirect(reverse_lazy('store_detail',kwargs={'pk': store.pk})+'?created=success')
        return HttpResponseRedirect(reverse_lazy('user_stores')+'?error')


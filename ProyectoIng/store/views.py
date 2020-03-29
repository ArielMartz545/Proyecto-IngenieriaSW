from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from ad.models import Category, PriceRange
from location.models import Location
from django.views.generic.edit import CreateView
from .models import Store, UsersXStore
from .forms import StoreForm
from django.http import  HttpResponseRedirect

# Create your views here.

class CreateStore(CreateView): #Pass,Correo,Nombre,Apellido,Telefono,Direccion,FechaN
    model = Store
    form_class=StoreForm
    template_name= 'store/my_stores.html' #Template al que envia el formulario
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['all_locations'] = Location.objects.all().order_by('direction')
        context['my_stores'] = UsersXStore.objects.prefetch_related('store').filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save()
            store.save()
            user_store = UsersXStore()
            user_store.user = request.user
            user_store.store = store
            user_store.save()
            return HttpResponseRedirect(reverse_lazy('my_stores')+'?added')
        return HttpResponseRedirect(reverse_lazy('my_stores')+'?error')
        
    def get_success_url(self):
        return reverse_lazy('my_stores')+'?added'
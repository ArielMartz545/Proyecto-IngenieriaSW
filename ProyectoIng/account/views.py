from django.shortcuts import redirect, render#Metodos de direccionamiento
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView #Objeto para la creacion de usuario, vista basada en Clase
from django.views.generic.base import TemplateView #Visualizacion de Template , Vista basada en Clase
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from account.models import Account #Modelo de Usuario
from account.forms import RegistrationForm, UpdateUserForm #Formulario de registro de usuario
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout, update_session_auth_hash  #Permite finalizar Sesion
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from ad.models import Category, PriceRange, Currency
from location.models import Location
from images.models import Image
from favorites.models import Favorites

# Create your views here.
class CreateUser(CreateView): #Pass,Correo,Nombre,Apellido,Telefono,Direccion,FechaN
    model = Account
    form_class=RegistrationForm
    template_name= 'registration/signup.html' #Template al que envia el formulario

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta.'
            message_html = render_to_string('registration/activation_mail.html', {
                'user': user.get_full_name(),
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            send_mail(mail_subject, strip_tags(message_html), settings.EMAIL_HOST_USER,[user.email],fail_silently=False,html_message=message_html)
            return HttpResponseRedirect(reverse_lazy('login')+'?register')
        return HttpResponse(render(request, 'registration/signup.html'))

    def get_success_url(self):
        return reverse_lazy('login')+'?register'
    
def update_user(request):
    #Solo solicitudes por metodo POST
    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES or None, instance=request.user)
        if form.is_valid():
            user = form.save()
            #Obtener la imagen de perfil si subio una, sino asigna valor de False a user_img_route
            user_img_route = request.FILES.get("user_img", False)
            #Obtener la imagen de portada si subio una, sino asigna valor de False a cover_img_route
            cover_img_route = request.FILES.get("cover_img", False)
            #Solo si se subio imagen de perfil
            if  user_img_route:
                #Si la imagen anterior es la imagen por defecto crear nuevo registro
                if  user.user_img.pk == 1:
                    user_img = Image(img_route = user_img_route)
                    user.user_img = user_img
                    user.user_img.save()
                #Si la imagen anterior no es la imagen por defecto modificar la ruta nada mas para evitar crear nuevos registros
                else:
                    user.user_img.img_route = user_img_route
                    user.user_img.save()
            #Solo si se subio imagen de portada
            if  cover_img_route:
                #Si la imagen anterior es la imagen por defecto crear nuevo registro
                if  user.cover_img.pk == 1:
                    cover_img = Image(img_route = cover_img_route)
                    user.cover_img = cover_img
                    user.cover_img.save()
                #Si la imagen anterior no es la imagen por defecto modificar la ruta nada mas para evitar crear nuevos registros
                else:
                    user.cover_img.img_route = cover_img_route
                    user.cover_img.save()
            user.save()
            return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': request.user.id})+'?update=success')
        else:
            return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': request.user.id})+'?update=error')
    #Cualquier otra redirige al perfil
    else:
        return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': request.user.id}))

def change_password(request):
    #Solo solicitudes por metodo POST
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesion, si esto no se hace causa un logout
            return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': request.user.id})+'?update=success')
        else:
            return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': request.user.id})+'?update=error')
    #Cualquier otra redirige al perfil
    else:
        return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': request.user.id}))

class DetailUser(DetailView):
    model = Account
    template_name = 'profile/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['all_locations'] = Location.objects.all().order_by('direction')
        context['currencies'] = Currency.objects.all()
        if  self.request.user.pk != self.kwargs['pk']:
            try:
                favorite = Favorites.objects.get(id_user__pk = self.request.user.pk, id_favorite_user__pk = self.kwargs['pk'])
            except:
                favorite = None
            if favorite is not None:
                context['favorite'] = True
            else:
                context['favorite'] = False
        else:
            context['favorite'] = False
        return context

    def get_success_url(self):
        return reverse_lazy('profile-view', kwargs={'pk': self.request.user.id})

        

class TemplateLogin(TemplateView):#Visualizar Login
    template_name = 'account/login.html'

def logout_view(request):#Cerrar Sesion
    logout(request)
    return redirect('login')

def politicas(request):
    return render(request, 'registration/privacy.html' )

def terminos(request):
    return render(request, 'registration/terms.html' )

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy('login')+'?activated')
    else:
        return HttpResponseRedirect(reverse_lazy('login')+'?invalid_activation')



    
from django.shortcuts import redirect, render#Metodos de direccionamiento
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView #Objeto para la creacion de usuario, vista basada en Clase
from django.views.generic.base import TemplateView #Visualizacion de Template , Vista basada en Clase
from account.models import Account #Modelo de Usuario
from account.forms import RegistrationForm #Formulario de registro de usuario
from django.contrib.auth import logout  #Permite finalizar Sesion
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

class TemplateLogin(TemplateView):#Visualizar Login
    template_name = 'account/login.html'

def logout_view(request):#Cerrar Sesion
    logout(request)
    return redirect('login')


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



    
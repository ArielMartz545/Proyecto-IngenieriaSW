"""ProyectoIng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from core.views import base_barra
from core import views

urlpatterns = [
    path('', base_barra.as_view(), name="home"),
    path('admin/', admin.site.urls),
    #Auth Paths
    path('accounts/',include('account.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('core/templates/core/privacy.html', views.privacy, name='privacy'),
    path('core/templates/core/terms.html', views.terms, name='terms'),

]

#Manejo de Imagenes en modo DEBUG
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
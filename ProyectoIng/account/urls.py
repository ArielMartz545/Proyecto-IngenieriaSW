from django.urls import path
from .views import * #CreateUser,TemplateLogin,logout_view, activate

urlpatterns = [
    path('signup',CreateUser.as_view(), name='signup'),#Template Registro
    path('login',TemplateLogin.as_view(), name='login'),#Template Login
    path('logout',logout_view, name='logout'),#Logout
    path('activate/<uidb64>/<token>',activate, name='activate'),#Activate account
    #path('url_bajo_account',vista en views, name='nombre'),
]
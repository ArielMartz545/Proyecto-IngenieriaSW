from django.urls import path
from .views import CreateUser,TemplateLogin,logout_view, activate, UpdateUser, DetailUser
from account import views

urlpatterns = [
    path('signup',CreateUser.as_view(), name='signup'),#Template Registro
    path('login',TemplateLogin.as_view(), name='login'),#Template Login
    path('logout',logout_view, name='logout'),#Logout
    path('activate/<uidb64>/<token>',activate, name='activate'),#Activate account
    #path('url_bajo_account',vista en views, name='nombre'),
    path('privacy', views.politicas, name='privacy'),
    path('terms', views.terminos, name='terms'),
    path('profile/<int:pk>', UpdateUser.as_view(), name='profile-edit'),
    path('profileS/<int:pk>', DetailUser.as_view(), name='profile-view'),
]
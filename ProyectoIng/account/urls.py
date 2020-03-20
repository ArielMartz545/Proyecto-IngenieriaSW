from django.urls import path
from account import views

urlpatterns = [
    path('signup',views.CreateUser.as_view(), name='signup'),#Template Registro
    path('login',views.TemplateLogin.as_view(), name='login'),#Template Login
    path('logout',views.logout_view, name='logout'),#Logout
    path('activate/<uidb64>/<token>',views.activate, name='activate'),#Activate account
    #path('url_bajo_account',vista en views, name='nombre'),
    path('privacy', views.politicas, name='privacy'),
    path('terms', views.terminos, name='terms'),
    path('profile/<int:pk>', views.DetailUser.as_view(), name='profile'),
    path('profile/update',views.update_user, name='profile-update'),
    path('profile/change-password',views.change_password, name='profile-change-password'),
]
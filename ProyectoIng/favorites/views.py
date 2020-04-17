from django.shortcuts import render, HttpResponse , HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Favorites
from account.models import Account

# Create your views here.
def ad_favorite(request):
    favorites= Favorites()

    #ID
    user = request.user.pk
    fav_user = request.POST.get('fav_user')
    #Instances
    user_instance= Account.objects.get(pk=user)
    fav_user_instance= Account.objects.get(pk=fav_user)
    #Asignation
    registred_favs_users= Favorites.objects.filter(id_user=user_instance).filter(id_favorite_user= fav_user_instance)
    print(registred_favs_users)

    if not registred_favs_users :
        favorites.id_user = user_instance
        favorites.id_favorite_user = fav_user_instance
        favorites.save()
    
    return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': fav_user}))
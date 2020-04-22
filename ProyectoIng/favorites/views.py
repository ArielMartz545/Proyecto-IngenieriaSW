from django.shortcuts import render, HttpResponse , HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Favorites
from account.models import Account

# Create your views here.
def ad_favorite(request):
    fav_user_pk = request.POST.get('fav_user')
    try:
        favorite = Favorites.objects.get(id_user__pk = request.user.pk, id_favorite_user__pk = fav_user_pk)
    except:
        favorite = None
    if favorite is not None:
        #Borrar de favoritos
        favorite.delete()
    else:
        #Agregar a favortos
        fav_user = Account.objects.get(pk=fav_user_pk)
        favorite = Favorites()
        favorite.id_user = request.user
        favorite.id_favorite_user = fav_user
        favorite.save()
    
    return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': fav_user_pk}))
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Rating
from .models import RatingStore
from .models import Store
from .models import Account
from django.db.models import Avg
# Create your views here.


def rate_user(request):
    #Recuperar datos de points y usuario que evalua por metodo POST
 
    if request.method == "POST":
        try:
            points = int( request.POST.get('id_points') )
        except:
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            evaluated_user_id = int( request.POST.get('id_evaluated_user') ) 
        except:
            return HttpResponseRedirect(reverse_lazy('home')) 
            
        comment = request.POST.get('id_comment')

        if comment is None:
            comment = ""

        try:
            evaluated_user = Account.objects.get(pk=evaluated_user_id) 
        except:
            return HttpResponseRedirect(reverse_lazy('home'))
  
        
        if  not (1 <= points <= 5): #Revisa si el puntaje no esta en el rango y lo regresa a perfil
            return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk':evaluated_user_id})+'?error=points'+ str(points))
        try:
            rating=Rating.objects.get(evaluated_user__pk = evaluated_user.pk, evaluator_user__pk = request.user.pk)
        except:
            rating = Rating(evaluated_user=evaluated_user, evaluator_user=request.user)

        
        rating.comment = comment
        rating.points = points
        rating.save()
        return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': evaluated_user_id}))

    else:
        return HttpResponseRedirect(reverse_lazy('home'))


def rate_store(request):
    if request.method == "POST":
        try:
            points = int( request.POST.get('id_points_store') )
        except:
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            evaluated_store_id = int( request.POST.get('id_evaluated_store'))
        except:
            return HttpResponseRedirect(reverse_lazy('home'))
        comment = request.POST.get('id_comment_store')
        if comment is None:
            comment = ""
        try:
            evaluated_store = Store.objects.get(pk=evaluated_store_id) 
        except:
            return HttpResponseRedirect(reverse_lazy('home'))
        if  not (1 <= points <= 5): #Revisa si el puntaje no esta en el rango y lo regresa a perfil
            return HttpResponseRedirect(reverse_lazy('store', kwargs={'pk':evaluated_store_id})+'?error=points'+ str(points))    
        try:
            ratingStore=RatingStore.objects.get(evaluated_store__pk = evaluated_store.pk, evaluator_user_store__pk = request.user.pk)
        except:
            ratingStore = RatingStore(evaluated_store=evaluated_store, evaluator_user_store=request.user)

        ratingStore.comment = comment
        ratingStore.points = points
        ratingStore.save()

        return HttpResponseRedirect(reverse_lazy('store_detail', kwargs={'pk': evaluated_store_id}))

    else:
        return HttpResponseRedirect(reverse_lazy('home'))

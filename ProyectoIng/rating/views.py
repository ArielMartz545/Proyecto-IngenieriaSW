from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Rating
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
            
        comments = request.POST.get('id_comment')

        if comments is None:
            comments = ""

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

        
        rating.comments = comments
        rating.points = points
        rating.save()
        return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': evaluated_user_id}))

    else:
        return HttpResponseRedirect(reverse_lazy('home'))


def rate_store(request):

    if request.method == "POST":
        try:
            points = int( request.POST.get('id_points') )
        except:
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            evaluated_store_id = int( request.POST.get('id_evaluated_user'))
        except:
            return HttpResponseRedirect(reverse_lazy('home'))
    
        comments = request.POST.get('id_comment')

        if comments is None:
            comments = ""

        try:
            evaluated_store = Account.objects.get(pk=evaluated_store_id) 
        except:
            return HttpResponseRedirect(reverse_lazy('home'))

        if  not (1 <= points <= 5): #Revisa si el puntaje no esta en el rango y lo regresa a perfil
            return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk':evaluated_store_id})+'?error=points'+ str(points))    
        try:
            rating=Rating.objects.get(evaluated_store__pk = evaluated_store.pk, evaluator_user__pk = request.user.pk)
        except:
            rating = Rating(evaluated_store=evaluated_store, evaluator_user=request.user)

        rating.comments = comments
        rating.points = points
        rating.save()

        return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': evaluated_store_id}))

    else:
        return HttpResponseRedirect(reverse_lazy('home'))


def prom(request):
    avss = average=Rating.objects.aggregate(avg('points'))
    return print(avss)
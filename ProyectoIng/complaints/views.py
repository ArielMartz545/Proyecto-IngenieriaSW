from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Complaint
from .models import Account
# Create your views here.


def complaint_user(request):
    #Recuperar datos de points y usuario que evalua por metodo POST
 
    if request.method == "POST":
        
        problem = request.POST.get('id_election')    
        comment = request.POST.get('id_comment')

        try:
            indicated_user_id = int( request.POST.get('id_indicated')) 
            indicated_user = Account.objects.get(pk=indicated_user_id) 
        except:
            return HttpResponseRedirect(reverse_lazy('home'))

        try:
            complaint = Complaint.objects.get(user_complaint = request.user.pk, indicated_user__pk = request.user.pk)
        except:
            complaint = Complaint(user_complaint=request.user, indicated_user=indicated_user)

        complaint.problem = problem
        complaint.comment = comment
        complaint.save()

        return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': indicated_user_id}))

    else:
        return HttpResponseRedirect(reverse_lazy('home'))
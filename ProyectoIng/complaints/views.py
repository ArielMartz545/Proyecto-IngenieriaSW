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
            complaint = Complaint.objects.get(user_complaint = request.user.pk)
        except:
            complaint = Complaint(user_complaint=request.user)

        complaint.problem = problem
        complaint.comment = comment
        complaint.save()
        return HttpResponseRedirect(reverse_lazy('home'))

    else:
        return HttpResponseRedirect(reverse_lazy('home'))
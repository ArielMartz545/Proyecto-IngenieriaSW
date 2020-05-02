from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.
class graphsTemplateView(TemplateView):
    template_name = "graphs/graphs.html"
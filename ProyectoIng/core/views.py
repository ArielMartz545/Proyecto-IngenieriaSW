from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.



class sidebar(TemplateView):

    template_name = "core/busquedas-sidebar-filtros.html"

class no_sidebar(TemplateView):

    template_name = "core/template-no-sidebarhtml.html"

class base_barra(TemplateView):

    template_name = "core/base-barra.html"

def privacy(request):
    return render_to_response('core/privacy.html', {}, RequestContext(request))

def terms(request):
    return render_to_response('core/terms.html', {}, RequestContext(request))




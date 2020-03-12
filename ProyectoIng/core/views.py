from django.shortcuts import render
from django.views.generic.base import TemplateView
from ad.models import Category, PriceRange
from location.models import Location
# Create your views here.

class main_page(TemplateView):
    template_name= "core/sidebar.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.filter(correlative_direction__isnull=True)
        return context


from django.urls import path
from .views import graphsTemplateView

urlpatterns = [
    path('estadistics/',graphsTemplateView.as_view(), name='graphs'),
    
]
from django.urls import path
from .views import ad_favorite


urlpatterns = [
    path('ad_favorite', ad_favorite , name="ad_favorite"),
]
from django.urls import path
from .views import ad_favorite , ad_favorite_store


urlpatterns = [
    path('ad_favorite', ad_favorite , name="ad_favorite"),
    path('ad_favorite_store', ad_favorite_store , name="ad_favorite_store"),
]
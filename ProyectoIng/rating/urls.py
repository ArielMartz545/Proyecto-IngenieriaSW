from django.urls import path
from .views import rate_user
from .views import rate_store


urlpatterns = [
    path('rate/user', rate_user, name="rate_user"),
    path('rate/store', rate_store, name="rate_store")
]
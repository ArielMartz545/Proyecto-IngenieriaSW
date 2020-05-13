from django.urls import path
from .views import complaint_user, complaint_store


urlpatterns = [
    path('complaint/user', complaint_user, name="complaint_user"),
    path('complaint/store', complaint_store, name="complaint_store"),
]
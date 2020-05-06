from django.urls import path
from .views import complaint_user


urlpatterns = [
    path('complaint/user', complaint_user, name="complaint_user"),
]
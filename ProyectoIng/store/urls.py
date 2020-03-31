from django.urls import path
from .views import CreateStore, UserStores

urlpatterns = [
    path('create',CreateStore.as_view(), name='create_store'),
    path('user/<uid>',UserStores.as_view(), name='user_stores'),
]
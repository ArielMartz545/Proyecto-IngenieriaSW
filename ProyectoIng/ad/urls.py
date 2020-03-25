from django.urls import path

from .views import ShowAdsListView, CategoryDetailView, AdDetailView, AdCreate, AdCreate2

urlpatterns = [
    path('', ShowAdsListView.as_view(), name='my_products'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name="category_products"),
    path('<int:pk>', AdDetailView.as_view(), name="ad_detail"),
    path('createad/', AdCreate, name="ad_create"),
    path('createad2/', AdCreate2, name="ad_create")
]
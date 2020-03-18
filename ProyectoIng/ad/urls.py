from django.urls import path

from .views import ShowAdsListView, CategoryDetailView

urlpatterns = [
    path('', ShowAdsListView.as_view(), name='my_products'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name="category_products"),
]
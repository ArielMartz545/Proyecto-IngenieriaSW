from django.urls import path
from .views import StoreAds, UserAds, CategoryAds, AdDetailView, CreateAd, AdUpdate, AdDelete

urlpatterns = [
    path('user/<int:uid>', UserAds.as_view(), name='products_user'),
    path('store/<int:sid>', StoreAds.as_view(), name='products_store'),
    path('category/<cid>', CategoryAds.as_view(), name='products_category'),
    path('<int:pk>', AdDetailView.as_view(), name="ad_detail"),
    path('create', CreateAd.as_view(), name="ad_create"),
    path('<int:pk>/update', AdUpdate.as_view(), name= "ad_update"),
    path('<int:pk>/delete', AdDelete.as_view(), name= "ad_delete"),
]
from django.urls import path

<<<<<<< Updated upstream
from .views import ShowAdsListView, CategoryDetailView, AdDetailView, CreateAd
=======
from .views import ShowAdsListView, CategoryDetailView, AdDetailView, CreateAd, AdUpdate, AdDelete
>>>>>>> Stashed changes

urlpatterns = [
    path('', ShowAdsListView.as_view(), name='my_products'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name="category_products"),
    path('<int:pk>', AdDetailView.as_view(), name="ad_detail"),
<<<<<<< Updated upstream
    path('create/', CreateAd.as_view(), name="ad_create")
=======
    path('create/', CreateAd.as_view(), name="ad_create"),
    path('<int:pk>/update', AdUpdate.as_view(), name= "ad_update"),
    path('<int:pk>/delete', AdDelete.as_view(), name= "ad_delete"),
>>>>>>> Stashed changes
]
from django.contrib import admin
from .models import Favorites, Favorites_Store
# Register your models here.

class FavoritesAdmin(admin.ModelAdmin):
    search_fields = ("id_user__first_name","id_user__last_name","id_user__email","id_favorite_user__first_name","id_favorite_user__last_name","id_favorite_user__email",)
class FavoritesAdmin_Store(admin.ModelAdmin):
    search_fields = ("id_user__first_name","id_user__last_name","id_user__email","id_favorite_store__store_name",)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Favorites_Store, FavoritesAdmin_Store)
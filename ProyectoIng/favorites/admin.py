from django.contrib import admin
from .models import Favorites
# Register your models here.

class FavoritesAdmin(admin.ModelAdmin):
    search_fields = ("id_user__first_name","id_user__last_name","id_user__email","id_favorite_user__first_name","id_favorite_user__last_name","id_favorite_user__email",)

admin.site.register(Favorites, FavoritesAdmin)
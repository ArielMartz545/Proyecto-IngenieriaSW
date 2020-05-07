from django.contrib import admin
from .models import Store, UsersXStore

# Register your models here.
class StorenAdmin(admin.ModelAdmin):
    search_fields = ("store_name","store_description","store_location__direction","store_location__correlative_direction__direction",)

class StoreXUserAdmin(admin.ModelAdmin):
    search_fields = ("store__store_name","store__store_description","store__store_location__direction","store__store_location__correlative_direction__direction",)

admin.site.register(Store,StorenAdmin)
admin.site.register(UsersXStore,StoreXUserAdmin)

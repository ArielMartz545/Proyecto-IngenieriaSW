from django.contrib import admin
from .models import Location

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    search_fields = ("direction","correlative_direction__direction",)

admin.site.register(Location,LocationAdmin)
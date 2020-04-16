from django.contrib import admin
from .models import Rating

# Register your models here.

#Codigo para mejorar la visualizacion del admin
class RatingAdmin(admin.ModelAdmin):
    list_display = ('evaluated_user','points', 'evaluator_user')

admin.site.register(Rating, RatingAdmin)
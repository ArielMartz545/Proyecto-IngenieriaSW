from django.contrib import admin
from .models import Rating
from .models import RatingStore

# Register your models here.

#Codigo para mejorar la visualizacion del admin
class RatingAdmin(admin.ModelAdmin):
    list_display = ('evaluated_user','points', 'evaluator_user')

class RatingStoreAdmin(admin.ModelAdmin):
    list_display = ('evaluated_store','points', 'evaluator_user_store')

admin.site.register(RatingStore, RatingStoreAdmin)
admin.site.register(Rating, RatingAdmin)
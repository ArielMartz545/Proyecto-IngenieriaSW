from django.contrib import admin
from .models import Category,AdKind, Ad, Unit, Currency, PriceRange

# Register your models here.
admin.site.register(Category)
admin.site.register(AdKind)
admin.site.register(Ad)
admin.site.register(Unit)
admin.site.register(Currency)
admin.site.register(PriceRange)

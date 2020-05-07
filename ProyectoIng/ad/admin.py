from django.contrib import admin
from .models import Category,AdKind, Ad, Unit, Currency, PriceRange, Disable_ads

# Register your models here.
admin.site.register(Category)
admin.site.register(AdKind)
admin.site.register(Ad)
admin.site.register(Unit)
admin.site.register(Currency)
admin.site.register(PriceRange)
admin.site.register(Disable_ads)

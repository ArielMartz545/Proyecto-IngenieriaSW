from django.contrib import admin
from .models import Category,AdKind, Ad, Unit, Currency, PriceRange, Disable_ads

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("category_name","category_description",)

class AdKindAdmin(admin.ModelAdmin):
    search_fields = ("ad_kind",)

class AdAdmin(admin.ModelAdmin):
    search_fields = ("ad_name","ad_description","price","id_user__first_name","id_user__email","id_user__last_name",)
    date_hierarchy = "date_created"
    list_display = ("ad_name" , "id_user","date_created")
    readonly_fields = ("date_created",)
    

    

class UnitAdmin(admin.ModelAdmin):
    search_fields = ("unit_type",)



admin.site.register(Category, CategoryAdmin)
admin.site.register(AdKind, AdKindAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Currency)
admin.site.register(PriceRange)
admin.site.register(Disable_ads)

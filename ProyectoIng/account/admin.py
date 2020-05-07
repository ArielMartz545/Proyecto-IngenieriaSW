from django.contrib import admin
from .models import Account,AccountManager

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined', )
    search_fields = ("first_name","last_name","email",)
 
admin.site.register(Account,AccountAdmin)
from django.contrib import admin
from .models import Account,AccountManager

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined', )
 
admin.site.register(Account,AccountAdmin)
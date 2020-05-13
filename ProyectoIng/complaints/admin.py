from django.contrib import admin
from .models import Complaint
from .models import ComplaintStore
# Register your models here.

class ComplaintsAdmin(admin.ModelAdmin):
    search_fields = ("problem","comment","user_complaint__first_name","user_complaint__email",)
    list_display = ('indicated_user','problem', 'published')

class ComplaintsStoreAdmin(admin.ModelAdmin):
    search_fields = ("problem","comment","reported_store__name",)
    list_display = ('reported_store','problem', 'published')

admin.site.register(Complaint, ComplaintsAdmin)
admin.site.register(ComplaintStore, ComplaintsStoreAdmin)


    
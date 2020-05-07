from django.contrib import admin
from .models import Complaint
# Register your models here.

class ComplaintsAdmin(admin.ModelAdmin):
    search_fields = ("problem","comment","user_complaint__first_name","user_complaint__email",)
    list_display = ('indicated_user','problem', 'published')

admin.site.register(Complaint, ComplaintsAdmin)


    
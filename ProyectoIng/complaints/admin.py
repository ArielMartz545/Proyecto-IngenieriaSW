from django.contrib import admin
from .models import Complaint
# Register your models here.

class ComplaintsAdmin(admin.ModelAdmin):

    list_display = ('problem', 'published')

admin.site.register(Complaint, ComplaintsAdmin)


from django import forms
from .models import Ad
from images.models import Image

class AdCreateForm(forms.ModelForm):
    
    class Meta():
        model= Ad
        fields=('ad_name', 'ad_description','price','id_location',
                'id_ad_kind','id_category','id_unit', 'id_currency',)

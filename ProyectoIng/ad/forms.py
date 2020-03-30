from django import forms
from .models import Ad
from images.models import Image

class AdCreateForm(forms.ModelForm):
    
    class Meta():
        model= Ad
        fields=('ad_name', 'ad_description','price','id_location',
                'id_ad_kind','id_category','id_unit', 'id_currency',)
<<<<<<< Updated upstream
=======

class AdUpdateForm(forms.ModelForm):
    
    class Meta():
        model = Ad
        fields=('ad_name', 'ad_description','price','id_location',
                'id_ad_kind','id_category','id_unit', 'id_currency',)
        widgets = {
            'ad_name': forms.TextInput (attrs={'class':'form-control'}),
            'ad_description': forms.Textarea (attrs={'class':'form-control'}),
            'price': forms.TextInput (attrs={'class':'form-control'}),
            'id_location': forms.Select(choices="Ubicacion",attrs={'class': 'form-control'}),
            'id_ad_kind': forms.Select(choices="Ubicacion",attrs={'class': 'form-control'}),
            'id_category': forms.Select(choices="Ubicacion",attrs={'class': 'form-control'}),
            'id_unit': forms.Select(choices="Ubicacion",attrs={'class': 'form-control'}),
            'id_currency': forms.Select(choices="Ubicacion",attrs={'class': 'form-control'}),
        }
        
class AdDeleteForm(forms.ModelForm):
    
    class Meta():
        model = Ad
        fields=('active',)
>>>>>>> Stashed changes

from django import forms
from .models import Ad
from images.models import Image

class AdCreateForm(forms.ModelForm):
    
    class Meta():
        model= Ad
        fields=('ad_name', 'ad_description','price','id_location',
                'id_ad_kind','id_category', 'id_currency',)


class AdUpdateForm(forms.ModelForm):
    
    class Meta():
        model = Ad
        #Campos del objeto para actualizar
        fields=('ad_name', 'ad_description','price','id_location',
                'id_ad_kind','id_category','id_unit', 'id_currency',)
        #Sustitucion de los nombres de los campos para ser mostrados al usuario
        labels={
            'ad_name':'Nombre del anuncio', 
            'ad_description':'Descripción de tu anuncio',
            'price':'Precio',
            'id_location':'Ubicación',
            'id_ad_kind':'Elige el tipo de anuncio',
            'id_category':'Selecciona la categoria de tu anuncio',
            'id_unit':'Unidad', 
            'id_currency':'Moneda'
        }
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

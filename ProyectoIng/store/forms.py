from django import forms
from .models import Store

# Create the form class.
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'store_description', 'store_location']

# Editando una tienda
class StoreUpdateForm(forms.ModelForm):
    class Meta():
        model = Store
        #Campos a actualizar en el formulario
        fields=('store_name', 'store_description', 'store_location', 'store_phone_number', 'store_website', 'store_email')
        #Nuevos labels para los campos, los que se muestran en el HTML al usuario
        labels = {
            'store_name':'Nombre de la tienda',
            'store_description':'Descripción de la tienda',
            'store_location':'Ubicación de la tienda',
            'store_phone_number':'Número de teléfono', 
            'store_website':'Sitio web', 
            'store_email':'Correo electrónico',
        }

#Eliminando una tienda
class StoreDeleteForm(forms.ModelForm):
    class Meta():
        model = Store
        fields=('active',)
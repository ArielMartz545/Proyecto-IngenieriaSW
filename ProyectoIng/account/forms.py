from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

#Redefine el formulario de creacion de usuario
class RegistrationForm(UserCreationForm):
    email= forms.EmailField(max_length=100,help_text='Se requiere un email valido.')

    class Meta(forms.ModelForm):
        model= Account
        fields= ("email","first_name","last_name","birth_date",
                "phone_number","password1",'password2',)

class UpdateUserForm(UserChangeForm):
    class Meta(forms.ModelForm):
        model= Account
        fields= ("first_name","last_name","birth_date",
                "phone_number","location","address")
                
        
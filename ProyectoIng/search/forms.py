from django import forms

class NameForm(forms.Form):
    min_price = forms.FloatField()
    max_price = forms.FloatField()
    location = forms.IntegerField()
    category = forms.IntegerField()
    search = forms.TextField()

    
from django import forms

from .models import SpineData


class ImageForm(forms.ModelForm):
    class Meta:
        model = SpineData
        fields = ('scale', 'image')

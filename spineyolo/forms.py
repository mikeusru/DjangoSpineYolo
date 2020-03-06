from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms

from .models import SpineData


class ImageForm(forms.ModelForm):

    class Meta:
        model = SpineData
        fields = ('scale', 'image')

from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import SpineData


class ImageForm(forms.ModelForm):
    class Meta:
        model = SpineData
        help_texts = {'scale': "pixels / μm"}
        fields = ('scale', 'image')


class RatingForm(forms.ModelForm):
    class Meta:
        model = SpineData
        fields = ('rating',)


RatingFormSet = inlineformset_factory(
    User,
    SpineData,
    form=RatingForm,
)

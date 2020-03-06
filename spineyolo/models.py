from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class SpineData(models.Model):
    scale = models.IntegerField(max_length=10)
    image = models.ImageField(upload_to="uploaded_spines/images", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.image.name

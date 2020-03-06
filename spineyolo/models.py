from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class SpineData(models.Model):
    scale = models.IntegerField()
    image = models.ImageField(upload_to="uploaded_spines/images", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    spine_coordinates_file = models.FileField(upload_to="analyzed_spines/coordinates", null=True)
    analysed_image = models.ImageField(upload_to="analyzed_spines/images", null=True)

    def __str__(self):
        return self.image.name

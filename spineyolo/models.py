from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


# Create your models here.
class SpineData(models.Model):
    scale = models.IntegerField()
    image = models.ImageField(upload_to="uploaded_spines/images", null=True)
    image_preview = models.ImageField(upload_to="uploaded_spines/preview_images", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    spine_coordinates_file = models.FileField(upload_to="analyzed_spines/coordinates", null=True)
    analyzed_image = models.ImageField(upload_to="analyzed_spines/images", null=True)

    def __str__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        if self.image and not self.image_preview:
            self.__create_png_preview()
        super(SpineData, self).save(*args, **kwargs)

    def __create_png_preview(self):
        img_name = "preview_image.png"
        img = Image.open(self.image)
        buffer = BytesIO()
        img.save(fp=buffer, format="PNG")
        content_file = ContentFile(buffer.getvalue())
        self.image_preview.save(img_name, InMemoryUploadedFile(
            content_file, None, img_name, 'image/png', content_file.tell,
            None
        ))
        return


def add_analyzed_image(pk, url):
    sd = SpineData.objects.get(pk=pk)
    temp_image = File(open(url, "rb"))
    sd.analyzed_image.save(url, temp_image)


def add_spine_coordinates(pk, url):
    sd = SpineData.objects.get(pk=pk)
    temp_file = File(open(url, "rb"))
    sd.spine_coordinates_file.save(url, temp_file)


def get_analyzed_image_url(pk):
    sd = SpineData.objects.get(pk=pk)
    return sd.analyzed_image.url


def get_coordinates_url(pk):
    sd = SpineData.objects.get(pk=pk)
    return sd.spine_coordinates_file.url

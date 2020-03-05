from django.conf.urls import url
from django.urls import include, path

from spineyolo import views

urlpatterns = [
    path('images/', views.ImageListView.as_view(), name='class_image_list'),
    path('images/upload', views.UploadImageView.as_view(), name='class_upload_image'),
]

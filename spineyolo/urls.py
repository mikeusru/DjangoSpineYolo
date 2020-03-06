from django.conf.urls import url
from django.urls import include, path

from spineyolo import views

app_name='spineyolo'

urlpatterns = [
    path('images/', views.ImageListView.as_view(), name='image_list'),
    path('images/analyze/<int:pk>', views.AnalyzeImageView.as_view(), name='analyze_image'),
    path('images/upload', views.UploadImageView.as_view(), name='upload_image'),
]

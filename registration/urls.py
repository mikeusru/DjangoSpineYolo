from django.urls import path

from registration import views

app_name = 'registration'
urlpatterns=[
    path('register/', views.RegisterView.as_view(), name='register'),
    path('index', views.index, name='index'),
    path('user_login/', views.user_login, name='user_login')
]
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from registration import views

app_name = 'registration'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('index', views.index, name='index'),
    path('user_login/', LoginView.as_view(), name='user_login'),
    path('logout/', views.logout_request, name='logout'),
]

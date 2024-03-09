from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('data', views.user_data_list, name='home'),
]

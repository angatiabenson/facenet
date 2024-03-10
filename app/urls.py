from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('data', views.user_data_list, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

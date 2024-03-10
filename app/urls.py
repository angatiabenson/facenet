from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('', views.user_data_list, name='home'),
    path('search-results', views.display_search_results, name='search_results'),
    path('search', views.upload_and_search, name='upload_and_search'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

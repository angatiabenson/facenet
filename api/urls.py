from django.urls import path
from .views import generate_face_metadata, compare_face_metadata

urlpatterns = [
    path('generate/face-metadata', generate_face_metadata,
         name='generate_face_metadata'),
    path('compare/face-metadata', compare_face_metadata,
         name='compare_face_metadata'),
]

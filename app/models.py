from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserData(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, default='')
    phone = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    region = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='user_images/')


class FaceMetadata(models.Model):
    user_data = models.OneToOneField(UserData, on_delete=models.CASCADE)
    face_encoding = models.TextField()

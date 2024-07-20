from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    image=models.ImageField(upload_to='profile-images/', blank=True, null=True, default='profile-images/default.png')
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'users'
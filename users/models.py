from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pictures/', default='default.jpg')
    bio = models.TextField(blank=True,null=True)
    phone = models.CharField(max_length=15, blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

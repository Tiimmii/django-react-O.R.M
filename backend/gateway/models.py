from django.db import models
from customuser.models import Customuser

# Create your models here.
class Jwt(models.Model):
    user = models.OneToOneField(Customuser, related_name='logged_in_user', on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Jwt Tokens"
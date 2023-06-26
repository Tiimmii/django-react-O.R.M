from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class Customusermanager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("username", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_head", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("is staff must be True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is superuser must be True")
        
        if extra_fields.get("is_head") is not True:
            raise ValueError("is head must be True")
        
        return self.create_user(email, password, **extra_fields)
        

class Customuser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_head = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = Customusermanager()

    def __str__(self):
        return self.email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class userManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):

        if not email:
            raise ValueError("User must provide email")
        if not username:
            raise ValueError("User must provide username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,  first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
         )
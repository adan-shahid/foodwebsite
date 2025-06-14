from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField



# Create your models here.

class userManager(BaseUserManager): #WE ARE EXTENDING THIS BASEUSERMANAGER, i.e, TAKING CONTROL OF IT.
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
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser): # WE ARE TAKING FULL CONTROL OF CUSTOM USER MODEL, INCLUDING AUTHENTICATI0N.
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique= True)
    phone = models.IntegerField(blank=True, null=True)

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)


    # REQUIRED FIELDS

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #WE USE EMAIL AS A LOGIN FIELD
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = userManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class UserProfile(models.Model):
#WE ARE PUTTING 1TO1 FIELD BCZ WE WANT THAT ONE USER SHOULD HAVE ONLY ONE PROFILE.
#IF WE WANT THE ONE USER TO HAVE MULTIPLE PROFILES, THEN WE USE FOREIGNKEY.
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city  = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email #WE ARE USING EMAIL AS A LOGIN FIELD.
    
#RIGHT NOW, WHEN WE MAKE USER, USER PROFILE IS NOT AUTOMATICALLY CREATED. 
#WE USE SIGNALS TO ACHIEVE THIS.

# SIGNALS ARE WRITTEN IN SEPARATE FILE i.e, signals.py
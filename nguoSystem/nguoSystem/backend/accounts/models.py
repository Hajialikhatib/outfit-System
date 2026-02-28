from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email inahitajika')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser lazima awe is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser lazima awe is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    
    GENDER_CHOICES = (
        ('kiume', 'Kiume'),
        ('kike', 'Kike'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Profile information
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Tailor-specific fields (kama mtu ni mshonaji)
    # is_staff=True maana ni mshonaji
    tailor_type = models.CharField(
        max_length=20,
        choices=(('kike', 'Nguo za Kike'), ('kiume', 'Nguo za Kiume'), ('zote', 'Zote')),
        null=True, blank=True,
        help_text='Chagua aina ya nguo unazoshona (kwa washonaji tu)'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, help_text='Je, mtu huyu ni mshonaji?')
    is_approved = models.BooleanField(default=False, help_text='Je, mshonaji amekubaliwa na admin?')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    @property
    def role(self):
        """Return user role based on permissions"""
        if self.is_superuser:
            return 'superuser'
        elif self.is_staff:
            return 'tailor'
        else:
            return 'customer'

    def save(self, *args, **kwargs):
        """Resize profile picture to max width 800px before saving"""
        if self.profile_picture:
            img = Image.open(self.profile_picture)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if width > 400px (smaller for profile pics)
            if img.width > 400:
                ratio = 400 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((400, new_height), Image.LANCZOS)
                
                # Save to BytesIO
                output = BytesIO()
                img.save(output, format='JPEG', quality=75, optimize=True)
                output.seek(0)
                
                # Replace the image file
                self.profile_picture = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{self.profile_picture.name.split('.')[0]}.jpg",
                    'image/jpeg',
                    sys.getsizeof(output),
                    None
                )
        
        super().save(*args, **kwargs)

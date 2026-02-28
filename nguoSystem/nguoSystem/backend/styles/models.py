from django.db import models
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Style(models.Model):
    GENDER_CHOICES = (
        ('kiume', 'Nguo za Kiume'),
        ('kike', 'Nguo za Kike'),
        ('zote', 'Nguo za Kiume na Kike'),
    )
    
    CATEGORY_CHOICES = (
        ('shati', 'Shati'),
        ('suruali', 'Suruali'),
        ('kanzu', 'Kanzu'),
        ('vitenge', 'Vitenge'),
        ('sare', 'Sare'),
        ('gauni', 'Gauni'),
        ('koti', 'Koti'),
        ('nyingine', 'Nyingine'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(help_text='Maelezo ya mtindo')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='zote')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='nyingine')
    image = models.ImageField(upload_to='styles/')
    tailor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='styles',
        help_text='Mshonaji aliyeunda mtindo huu'
    )
    is_approved = models.BooleanField(
        default=False, 
        help_text='Je, mtindo umekubaliwa na admin?'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mtindo'
        verbose_name_plural = 'Mitindo'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Resize image to max width 800px before saving"""
        if self.image:
            img = Image.open(self.image)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if width > 600px (reduced for faster loading)
            if img.width > 600:
                # Calculate new height to maintain aspect ratio
                ratio = 600 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((600, new_height), Image.LANCZOS)
                
                # Save to BytesIO
                output = BytesIO()
                img.save(output, format='JPEG', quality=80, optimize=True)
                output.seek(0)
                
                # Replace the image file
                self.image = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{self.image.name.split('.')[0]}.jpg",
                    'image/jpeg',
                    sys.getsizeof(output),
                    None
                )
        
        super().save(*args, **kwargs)

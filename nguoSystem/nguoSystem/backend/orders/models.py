from django.db import models
from django.conf import settings
from styles.models import Style
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Order(models.Model):
    SIZE_CHOICES = (
        ('NDOGO', 'Ndogo'),
        ('KATI', 'Saizi ya Kati'),
        ('KUBWA', 'Kubwa'),
        ('CUSTOM', 'Vipimo maalum'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Inasubiri'),
        ('APPROVED', 'Imekubaliwa'),
        ('IN_PROGRESS', 'Inaendelea'),
        ('COMPLETED', 'Imemaliza'),
        ('DELIVERED', 'Imetumwa'),
        ('REJECTED', 'Imekataliwa'),
        ('CANCELLED', 'Imesitishwa'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_orders', verbose_name='Mteja')
    tailor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tailor_orders', verbose_name='Mshonaji')
    style = models.ForeignKey(Style, on_delete=models.CASCADE, null=True, blank=True)
    custom_style = models.TextField(null=True, blank=True, help_text='Maelezo ya mtindo maalum')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Idadi')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    
    # Vipimo (Measurements)
    kifua = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Kipimo cha kifua (cm)')
    mkono = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Urefu wa mkono (cm)')
    kiuno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Kipimo cha kiuno (cm)')
    mguu = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Urefu wa mguu (cm)')
    urefu = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Urefu wa jumla (cm)')
    shingo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Kipimo cha shingo (cm)')
    
    # Price and delivery
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True, help_text='Tarehe ya kupokea nguo')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Oda'
        verbose_name_plural = 'Oda'
    
    def __str__(self):
        return f"Oda #{self.pk} - {self.customer.full_name}"
    
    def can_delete(self):
        """Check if order can be deleted (within 3 days of creation)"""
        from datetime import timedelta
        from django.utils import timezone
        return timezone.now() <= self.created_at + timedelta(days=3)

    def save(self, *args, **kwargs):
        """Calculate total price if quantity and style are set"""
        if self.style and self.quantity and not self.total_price:
            self.total_price = self.style.price * self.quantity
        super().save(*args, **kwargs)


class CustomStyleRequest(models.Model):
    """
    Custom Style Request Model
    ==========================
    When a user doesn't find a preferred style, they can upload a custom style request.
    Admin can approve or reject the request.
    """
    
    STATUS_CHOICES = (
        ('PENDING', 'Inasubiri'),
        ('APPROVED', 'Imekubaliwa'),
        ('REJECTED', 'Imekataliwa'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='custom_style_requests',
        verbose_name='Mteja'
    )
    image = models.ImageField(
        upload_to='custom_styles/',
        verbose_name='Picha ya Mtindo',
        help_text='Pakia picha ya mtindo unaotaka'
    )
    description = models.TextField(
        verbose_name='Maelezo',
        help_text='Eleza mtindo unaoutaka kwa undani'
    )
    preferred_fabric = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Kitambaa Kinachopendwa',
        help_text='Andika aina ya kitambaa unalopenda (kama unalijua)'
    )
    estimated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Bei ya Makadirio',
        help_text='Bei iliyokadiriwa na mshonaji'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Hali'
    )
    admin_notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Maoni ya Admin',
        help_text='Maoni kutoka kwa mshonaji'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarehe ya Kuunda')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Tarehe ya Kubadilisha')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ombi la Mtindo Maalum'
        verbose_name_plural = 'Maombi ya Mitindo Maalum'

    def save(self, *args, **kwargs):
        """Resize custom style image to max width 600px before saving"""
        if self.image:
            img = Image.open(self.image)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if width > 600px
            if img.width > 600:
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
    
    def __str__(self):
        return f"Ombi la Mtindo Maalum #{self.pk} - {self.user.full_name}"


class Comment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='comment')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maoni ya Oda #{self.order.pk}"


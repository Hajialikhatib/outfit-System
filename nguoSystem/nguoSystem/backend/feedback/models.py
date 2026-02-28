"""
Feedback Models
===============
This module contains the Feedback model for user reviews after order approval.
Users can only submit feedback after their order is approved.
"""

from django.db import models
from django.conf import settings
from orders.models import Order


class Feedback(models.Model):
    """
    Feedback model - Users can submit feedback only after their order is approved.
    
    Fields:
    - user: The user who submitted the feedback
    - order: The order this feedback is for (must be approved)
    - message: The feedback message
    - rating: Optional star rating (1-5)
    - created_at: When the feedback was submitted
    """
    
    RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Mteja'
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='feedback',
        verbose_name='Oda'
    )
    message = models.TextField(
        verbose_name='Maoni',
        help_text='Andika maoni yako kuhusu huduma uliyopata'
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True,
        verbose_name='Kiwango',
        help_text='Kiwango cha kuridhika (1-5)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Tarehe ya kuwasilisha'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Maoni'
        verbose_name_plural = 'Maoni'
    
    def __str__(self):
        return f"Maoni ya {self.user.full_name} - Oda #{self.order.pk}"
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure feedback is only submitted for approved orders.
        """
        if self.order.status not in ['APPROVED', 'COMPLETED', 'DELIVERED']:
            raise ValueError('Maoni yanaweza kutumwa tu kwa oda zilizokubaliwa')
        super().save(*args, **kwargs)

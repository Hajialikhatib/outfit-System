"""
Feedback Admin
==============
Admin configuration for Feedback model.
"""

from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Admin configuration for Feedback model."""
    
    list_display = ['id', 'user', 'order', 'rating', 'short_message', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__email', 'user__full_name', 'message']
    readonly_fields = ['user', 'order', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Taarifa za Maoni', {
            'fields': ('user', 'order', 'message', 'rating')
        }),
        ('Tarehe', {
            'fields': ('created_at',)
        }),
    )
    
    def short_message(self, obj):
        """Display truncated message in list view."""
        if len(obj.message) > 50:
            return obj.message[:50] + '...'
        return obj.message
    short_message.short_description = 'Maoni'
    
    def has_add_permission(self, request):
        """Disable adding feedback from admin - must be done via frontend."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing feedback."""
        return False

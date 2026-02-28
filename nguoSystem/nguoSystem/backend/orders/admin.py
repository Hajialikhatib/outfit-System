from django.contrib import admin
from .models import Order, Comment, CustomStyleRequest


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'style', 'size', 'status', 'total_price', 'delivery_date', 'created_at']
    list_filter = ['status', 'size', 'created_at']
    search_fields = ['customer__email', 'customer__full_name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'delivery_date']
    
    fieldsets = (
        ('Taarifa za Oda', {
            'fields': ('customer', 'tailor', 'style', 'custom_style', 'quantity', 'size', 'status')
        }),
        ('Vipimo', {
            'fields': ('kifua', 'mkono', 'kiuno', 'mguu', 'urefu', 'shingo')
        }),
        ('Malipo na Utoaji', {
            'fields': ('total_price', 'delivery_date')
        }),
        ('Tarehe', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_orders', 'reject_orders']
    
    @admin.action(description='Kubali oda zilizochaguliwa')
    def approve_orders(self, request, queryset):
        updated = queryset.update(status='APPROVED')
        self.message_user(request, f'Oda {updated} zimekubaliwa.')
    
    @admin.action(description='Kataa oda zilizochaguliwa')
    def reject_orders(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f'Oda {updated} zimekataliwa.')


@admin.register(CustomStyleRequest)
class CustomStyleRequestAdmin(admin.ModelAdmin):
    """Admin for Custom Style Requests."""
    list_display = ['id', 'user', 'status', 'estimated_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'user__full_name', 'description']
    readonly_fields = ['user', 'image', 'description', 'preferred_fabric', 'created_at', 'updated_at']
    list_editable = ['status', 'estimated_price']
    
    fieldsets = (
        ('Taarifa za Ombi', {
            'fields': ('user', 'image', 'description', 'preferred_fabric')
        }),
        ('Usimamizi', {
            'fields': ('status', 'estimated_price', 'admin_notes')
        }),
        ('Tarehe', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    @admin.action(description='Kubali maombi yaliyochaguliwa')
    def approve_requests(self, request, queryset):
        updated = queryset.update(status='APPROVED')
        self.message_user(request, f'Maombi {updated} yamekubaliwa.')
    
    @admin.action(description='Kataa maombi yaliyochaguliwa')
    def reject_requests(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f'Maombi {updated} yamekataliwa.')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['order', 'message', 'created_at']
    search_fields = ['order__user__email', 'message']
    readonly_fields = ['created_at', 'updated_at']


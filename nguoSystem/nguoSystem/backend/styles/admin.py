from django.contrib import admin
from .models import Style


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'category', 'price', 'created_at']
    list_filter = ['gender', 'category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['price']

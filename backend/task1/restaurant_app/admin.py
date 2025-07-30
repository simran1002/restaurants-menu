from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'phone_number', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['name', 'address', 'phone_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

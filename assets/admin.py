from django.contrib import admin
from .models import Asset, UserProfile, AuditLog, SupportTicket


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'asset_type', 'manufacturer', 'model', 'product_name', 'status', 'assigned_to', 'date_in_service']
    list_filter = ['asset_type', 'status']
    search_fields = ['manufacturer', 'model', 'serial_number', 'asset_tag', 'product_name']
    list_editable = ['status']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'asset', 'user', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    readonly_fields = ['asset', 'user', 'action', 'timestamp', 'details']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'asset', 'title', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
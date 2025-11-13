from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extended user profile with role information.
    Linked to Django's built-in User model.
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('technician', 'Technician'),
        ('user', 'End User'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Asset(models.Model):
    """
    Represents an inventory asset (physical or digital).
    Implements Epic 1: Asset Lifecycle Management
    """
    ASSET_TYPE_CHOICES = [
        ('physical', 'Physical Asset'),
        ('digital', 'Digital Asset'),
    ]
    
    STATUS_CHOICES = [
        ('in_service', 'In Service'),
        ('out_repair', 'Out for Repair'),
        ('decommissioned', 'Decommissioned'),
    ]
    
    # Common fields
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_service')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    date_in_service = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Physical asset fields
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, unique=True, null=True)
    asset_tag = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Digital asset fields
    product_name = models.CharField(max_length=200, blank=True)
    license_key = models.CharField(max_length=200, blank=True)
    version = models.CharField(max_length=50, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    
    # Repair tracking
    repair_notes = models.TextField(blank=True)
    
    def __str__(self):
        if self.asset_type == 'physical':
            return f"{self.manufacturer} {self.model} - {self.asset_tag}"
        else:
            return f"{self.product_name} - {self.license_key}"
    
    class Meta:
        ordering = ['-created_at']


class AuditLog(models.Model):
    """
    Immutable audit log for tracking asset changes.
    Implements Epic 5: Data Integrity & Auditing
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='audit_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    
    def __str__(self):
        return f"{self.action} on {self.asset} by {self.user} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']


class SupportTicket(models.Model):
    """
    Support tickets linked to assets.
    Implements Epic 4: Integration with Support Ticketing System
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='tickets')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tickets')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Ticket #{self.id}: {self.title} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
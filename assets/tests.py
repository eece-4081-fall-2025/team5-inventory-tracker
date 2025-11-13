from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from .models import Asset, UserProfile, AuditLog, SupportTicket


class AssetLifecycleTests(TestCase):
    """
    Epic 1: Asset Lifecycle Management
    Tests asset creation, assignment, status changes, and decommissioning
    Author: Matthew J.
    """
    
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(username='admin', password='test123')
        self.tech_user = User.objects.create_user(username='tech', password='test123')
        self.end_user = User.objects.create_user(username='enduser', password='test123')
        
        # Create user profiles
        UserProfile.objects.create(user=self.admin_user, role='admin')
        UserProfile.objects.create(user=self.tech_user, role='technician')
        UserProfile.objects.create(user=self.end_user, role='user')
    
    def test_create_physical_asset(self):
        """Test creating a physical asset"""
        asset = Asset.objects.create(
            asset_type='physical',
            manufacturer='Dell',
            model='Latitude 5420',
            serial_number='SN123456',
            asset_tag='ASSET001',
            location='Building A, Floor 2',
            status='in_service'
        )
        self.assertEqual(asset.asset_type, 'physical')
        self.assertEqual(asset.status, 'in_service')
        self.assertIsNotNone(asset.date_in_service)
    
    def test_create_digital_asset(self):
        """Test creating a digital asset"""
        asset = Asset.objects.create(
            asset_type='digital',
            product_name='Microsoft Office 365',
            license_key='XXXXX-XXXXX-XXXXX',
            version='2024',
            renewal_date=date.today() + timedelta(days=365),
            status='in_service'
        )
        self.assertEqual(asset.asset_type, 'digital')
        self.assertEqual(asset.product_name, 'Microsoft Office 365')
    
    def test_assign_asset_to_user(self):
        """Test assigning an asset to an end user"""
        asset = Asset.objects.create(
            asset_type='physical',
            manufacturer='Apple',
            model='MacBook Pro',
            serial_number='SN789012',
            asset_tag='ASSET002'
        )
        asset.assigned_to = self.end_user
        asset.save()
        
        self.assertEqual(asset.assigned_to, self.end_user)
        self.assertEqual(self.end_user.assets.count(), 1)
    
    def test_change_asset_status_to_repair(self):
        """Test changing asset status to out for repair"""
        asset = Asset.objects.create(
            asset_type='physical',
            manufacturer='HP',
            model='EliteBook 840',
            serial_number='SN345678',
            status='in_service'
        )
        asset.status = 'out_repair'
        asset.repair_notes = 'Screen cracked, needs replacement'
        asset.save()
        
        self.assertEqual(asset.status, 'out_repair')
        self.assertIn('Screen cracked', asset.repair_notes)
    
    def test_return_asset_to_service(self):
        """Test returning a repaired asset back to service"""
        asset = Asset.objects.create(
            asset_type='physical',
            manufacturer='Lenovo',
            model='ThinkPad X1',
            serial_number='SN901234',
            status='out_repair',
            repair_notes='Battery issue'
        )
        asset.status = 'in_service'
        asset.repair_notes += ' | Repair completed: Battery replaced'
        asset.save()
        
        self.assertEqual(asset.status, 'in_service')
        self.assertIn('Battery replaced', asset.repair_notes)
    
    def test_decommission_asset(self):
        """Test decommissioning an asset"""
        asset = Asset.objects.create(
            asset_type='physical',
            manufacturer='Dell',
            model='OptiPlex 7080',
            serial_number='SN567890',
            status='in_service'
        )
        asset.status = 'decommissioned'
        asset.save()
        
        self.assertEqual(asset.status, 'decommissioned')


class UserPermissionsTests(TestCase):
    """
    Epic 2: User Permissions & Access Control
    Tests role-based access and user profiles
    Author: Carlin W.
    """
    
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin123')
        self.tech = User.objects.create_user(username='tech', password='tech123')
        self.user = User.objects.create_user(username='user', password='user123')
        
        self.admin_profile = UserProfile.objects.create(user=self.admin, role='admin')
        self.tech_profile = UserProfile.objects.create(user=self.tech, role='technician')
        self.user_profile = UserProfile.objects.create(user=self.user, role='user')
    
    def test_user_profile_creation(self):
        """Test creating user profiles with different roles"""
        self.assertEqual(self.admin_profile.role, 'admin')
        self.assertEqual(self.tech_profile.role, 'technician')
        self.assertEqual(self.user_profile.role, 'user')
    
    def test_admin_can_manage_all_assets(self):
        """Test that admin role is properly assigned"""
        self.assertEqual(self.admin.profile.role, 'admin')
    
    def test_technician_role(self):
        """Test that technician role is properly assigned"""
        self.assertEqual(self.tech.profile.role, 'technician')
    
    def test_end_user_role(self):
        """Test that end user role is properly assigned"""
        self.assertEqual(self.user.profile.role, 'user')


class SearchAndReportingTests(TestCase):
    """
    Epic 3: Search, Reporting & Analytics
    Tests asset search and reporting functionality
    Author: Rohith R.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        
        # Create multiple assets for testing
        Asset.objects.create(
            asset_type='physical',
            manufacturer='Dell',
            model='Laptop',
            serial_number='SN001',
            asset_tag='TAG001',
            status='in_service',
            assigned_to=self.user
        )
        Asset.objects.create(
            asset_type='physical',
            manufacturer='HP',
            model='Desktop',
            serial_number='SN002',
            asset_tag='TAG002',
            status='out_repair'
        )
        Asset.objects.create(
            asset_type='digital',
            product_name='Adobe Creative Cloud',
            license_key='KEY001',
            status='in_service',
            assigned_to=self.user
        )
    
    def test_filter_assets_by_status(self):
        """Test filtering assets by status"""
        in_service = Asset.objects.filter(status='in_service')
        out_repair = Asset.objects.filter(status='out_repair')
        
        self.assertEqual(in_service.count(), 2)
        self.assertEqual(out_repair.count(), 1)
    
    def test_filter_assets_by_type(self):
        """Test filtering assets by type"""
        physical = Asset.objects.filter(asset_type='physical')
        digital = Asset.objects.filter(asset_type='digital')
        
        self.assertEqual(physical.count(), 2)
        self.assertEqual(digital.count(), 1)
    
    def test_search_by_manufacturer(self):
        """Test searching assets by manufacturer"""
        dell_assets = Asset.objects.filter(manufacturer__icontains='Dell')
        self.assertEqual(dell_assets.count(), 1)
    
    def test_assets_assigned_to_user(self):
        """Test retrieving all assets assigned to a specific user"""
        user_assets = Asset.objects.filter(assigned_to=self.user)
        self.assertEqual(user_assets.count(), 2)
    
    def test_get_asset_statistics(self):
        """Test generating asset statistics"""
        total_assets = Asset.objects.count()
        in_service = Asset.objects.filter(status='in_service').count()
        out_repair = Asset.objects.filter(status='out_repair').count()
        
        self.assertEqual(total_assets, 3)
        self.assertEqual(in_service, 2)
        self.assertEqual(out_repair, 1)


class SupportTicketIntegrationTests(TestCase):
    """
    Epic 4: Integration with Support Ticketing System
    Tests support ticket creation and management
    Author: Matthew J.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='test123')
        self.asset = Asset.objects.create(
            asset_type='physical',
            manufacturer='Dell',
            model='Monitor',
            serial_number='SN999',
            status='in_service',
            assigned_to=self.user
        )
    
    def test_create_support_ticket(self):
        """Test creating a support ticket for an asset"""
        ticket = SupportTicket.objects.create(
            asset=self.asset,
            created_by=self.user,
            title='Monitor not turning on',
            description='The monitor does not power on when pressed',
            status='open'
        )
        self.assertEqual(ticket.status, 'open')
        self.assertEqual(ticket.asset, self.asset)
        self.assertEqual(ticket.created_by, self.user)
    
    def test_update_ticket_status(self):
        """Test updating a support ticket status"""
        ticket = SupportTicket.objects.create(
            asset=self.asset,
            created_by=self.user,
            title='Keyboard issue',
            description='Some keys not working',
            status='open'
        )
        ticket.status = 'in_progress'
        ticket.save()
        
        self.assertEqual(ticket.status, 'in_progress')
    
    def test_resolve_ticket(self):
        """Test resolving a support ticket"""
        ticket = SupportTicket.objects.create(
            asset=self.asset,
            created_by=self.user,
            title='Software installation',
            description='Need software installed',
            status='open'
        )
        ticket.status = 'resolved'
        ticket.resolved_at = timezone.now()
        ticket.save()
        
        self.assertEqual(ticket.status, 'resolved')
        self.assertIsNotNone(ticket.resolved_at)
    
    def test_asset_has_multiple_tickets(self):
        """Test that an asset can have multiple tickets"""
        SupportTicket.objects.create(
            asset=self.asset,
            created_by=self.user,
            title='Ticket 1',
            description='Description 1',
            status='open'
        )
        SupportTicket.objects.create(
            asset=self.asset,
            created_by=self.user,
            title='Ticket 2',
            description='Description 2',
            status='resolved'
        )
        
        self.assertEqual(self.asset.tickets.count(), 2)


class AuditLogTests(TestCase):
    """
    Epic 5: Data Integrity & Auditing
    Tests immutable audit logging functionality
    Author: Carlin W.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='auditor', password='test123')
        self.asset = Asset.objects.create(
            asset_type='physical',
            manufacturer='Apple',
            model='iMac',
            serial_number='SN888',
            status='in_service'
        )
    
    def test_create_audit_log(self):
        """Test creating an audit log entry"""
        log = AuditLog.objects.create(
            asset=self.asset,
            user=self.user,
            action='created',
            details='Asset created in system'
        )
        self.assertEqual(log.action, 'created')
        self.assertEqual(log.asset, self.asset)
        self.assertEqual(log.user, self.user)
    
    def test_log_status_change(self):
        """Test logging asset status changes"""
        log = AuditLog.objects.create(
            asset=self.asset,
            user=self.user,
            action='status_changed',
            details='Status changed from in_service to out_repair'
        )
        self.assertEqual(log.action, 'status_changed')
        self.assertIn('out_repair', log.details)
    
    def test_log_assignment_change(self):
        """Test logging asset assignment changes"""
        new_user = User.objects.create_user(username='newuser', password='test123')
        log = AuditLog.objects.create(
            asset=self.asset,
            user=self.user,
            action='assigned',
            details=f'Asset assigned to {new_user.username}'
        )
        self.assertEqual(log.action, 'assigned')
        self.assertIn('newuser', log.details)
    
    def test_audit_log_chronological_order(self):
        """Test that audit logs are in chronological order"""
        AuditLog.objects.create(asset=self.asset, user=self.user, action='created', details='First')
        AuditLog.objects.create(asset=self.asset, user=self.user, action='updated', details='Second')
        AuditLog.objects.create(asset=self.asset, user=self.user, action='deleted', details='Third')
        
        logs = AuditLog.objects.filter(asset=self.asset)
        self.assertEqual(logs.count(), 3)
        # Most recent should be first (descending order)
        self.assertEqual(logs[0].details, 'Third')


class DataOnboardingTests(TestCase):
    """
    Epic 6: System Setup & Data Onboarding
    Tests bulk import and initial setup functionality
    Author: Rohith R.
    """
    
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin123')
        UserProfile.objects.create(user=self.admin, role='admin')
    
    def test_bulk_asset_creation(self):
        """Test creating multiple assets at once (simulating CSV import)"""
        assets_data = [
            {'asset_type': 'physical', 'manufacturer': 'Dell', 'model': 'Laptop1', 'serial_number': 'S001'},
            {'asset_type': 'physical', 'manufacturer': 'HP', 'model': 'Laptop2', 'serial_number': 'S002'},
            {'asset_type': 'digital', 'product_name': 'Office365', 'license_key': 'KEY1'},
        ]
        
        for data in assets_data:
            Asset.objects.create(**data)
        
        self.assertEqual(Asset.objects.count(), 3)
    
    def test_initial_user_setup(self):
        """Test setting up initial users with roles"""
        tech = User.objects.create_user(username='tech1', password='tech123')
        user = User.objects.create_user(username='user1', password='user123')
        
        UserProfile.objects.create(user=tech, role='technician')
        UserProfile.objects.create(user=user, role='user')
        
        self.assertEqual(UserProfile.objects.count(), 3)  # Including admin from setUp
    
    def test_validate_unique_serial_numbers(self):
        """Test that serial numbers must be unique"""
        Asset.objects.create(
            asset_type='physical',
            manufacturer='Dell',
            model='Desktop',
            serial_number='UNIQUE123'
        )
        
        # Attempting to create another asset with the same serial number should fail
        with self.assertRaises(Exception):
            Asset.objects.create(
                asset_type='physical',
                manufacturer='HP',
                model='Laptop',
                serial_number='UNIQUE123'
            )
    
    def test_asset_default_status(self):
        """Test that assets default to 'in_service' status"""
        asset = Asset.objects.create(
            asset_type='physical',
            manufacturer='Apple',
            model='MacBook',
            serial_number='SN555'
        )
        self.assertEqual(asset.status, 'in_service')
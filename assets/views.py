from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json
from .models import Asset, UserProfile


def index(request):
    """Serve the main HTML page"""
    return render(request, 'index.html')


@csrf_exempt
def api_login(request):
    """Handle login requests from JavaScript"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # Map usernames to IDs to match the demo users
            user_map = {
                'admin': {'id': 1, 'name': 'Admin User', 'role': 'admin'},
                'tech': {'id': 2, 'name': 'Tech User', 'role': 'technician'},
                'johndoe': {'id': 3, 'name': 'John Doe', 'role': 'user'},
                'janesmith': {'id': 4, 'name': 'Jane Smith', 'role': 'user'},
            }
            
            # Get user info or default to generic user
            user_info = user_map.get(username.lower(), {
                'id': 3,  # Default to John Doe ID
                'name': username,
                'role': 'user'
            })
            
            return JsonResponse({
                'success': True,
                'user': user_info
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt  
def api_assets_list(request):
    """Get all assets or create new asset"""
    if request.method == 'GET':
        assets = Asset.objects.all()
        assets_data = []
        
        for asset in assets:
            asset_dict = {
                'id': asset.id,
                'type': asset.asset_type,
                'status': 'In Service' if asset.status == 'in_service' else 'Out for Repair',
                'assigneeId': asset.assigned_to.id if asset.assigned_to else None,
                'assigneeName': asset.assigned_to.username if asset.assigned_to else 'Unassigned',
                'dateInService': str(asset.date_in_service),
                'repairNotes': asset.repair_notes,
            }
            
            if asset.asset_type == 'physical':
                asset_dict.update({
                    'manufacturer': asset.manufacturer,
                    'model': asset.model,
                    'serialNumber': asset.serial_number or '',
                    'assetTag': asset.asset_tag,
                    'location': asset.location,
                })
            else:
                asset_dict.update({
                    'productName': asset.product_name,
                    'licenseKey': asset.license_key,
                    'version': asset.version,
                    'renewalDate': str(asset.renewal_date) if asset.renewal_date else '',
                })
            
            assets_data.append(asset_dict)
        
        return JsonResponse({'assets': assets_data})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create new asset
            asset_data = {
                'asset_type': data.get('type'),
                'status': 'in_service' if data.get('status') == 'In Service' else 'out_repair',
            }
            
            # Add assigned user if provided
            if data.get('assigneeId'):
                try:
                    user = User.objects.get(id=data['assigneeId'])
                    asset_data['assigned_to'] = user
                except:
                    pass
            
            # Add type-specific fields
            if data.get('type') == 'physical':
                asset_data.update({
                    'manufacturer': data.get('manufacturer', ''),
                    'model': data.get('model', ''),
                    'serial_number': data.get('serialNumber'),
                    'asset_tag': data.get('assetTag', ''),
                    'location': data.get('location', ''),
                })
            else:
                asset_data.update({
                    'product_name': data.get('productName', ''),
                    'license_key': data.get('licenseKey', ''),
                    'version': data.get('version', ''),
                    'renewal_date': data.get('renewalDate') if data.get('renewalDate') else None,
                })
            
            asset = Asset.objects.create(**asset_data)
            
            return JsonResponse({'success': True, 'asset_id': asset.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False})


@csrf_exempt
def api_asset_detail(request, asset_id):
    """Update or delete specific asset"""
    try:
        asset = Asset.objects.get(id=asset_id)
        
        if request.method == 'PUT':
            data = json.loads(request.body)
            
            # Update status
            if 'status' in data:
                status_value = data['status']
                asset.status = 'in_service' if status_value == 'In Service' else 'out_repair'
            
            # Update repair notes
            if 'repairNotes' in data:
                asset.repair_notes = data['repairNotes']
            
            asset.save()
            return JsonResponse({'success': True})
        
        elif request.method == 'DELETE':
            asset.delete()
            return JsonResponse({'success': True})
        
    except Asset.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Asset not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False})


@csrf_exempt
def api_users_list(request):
    """Get all users for assignment dropdown"""
    # Return demo users for now
    users_data = {
        'users': [
            {'id': 1, 'username': 'admin', 'name': 'Admin User', 'role': 'admin'},
            {'id': 2, 'username': 'tech', 'name': 'Tech User', 'role': 'technician'},
            {'id': 3, 'username': 'johndoe', 'name': 'John Doe', 'role': 'user'},
            {'id': 4, 'username': 'janesmith', 'name': 'Jane Smith', 'role': 'user'},
        ]
    }
    
    return JsonResponse(users_data)
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json

# Placeholder views for emergencies app
# These will be implemented with proper functionality later

def emergency_list(request):
    """List all emergencies"""
    # Sample data for testing frontend connectivity
    sample_emergencies = [
        {
            'id': 1,
            'emergency_id': 'EMS-2025-001',
            'severity': 'critical',
            'status': 'dispatched',
            'location': '37.7749,-122.4194',
            'reported_at': '2025-09-27T10:00:00Z',
            'description': 'Cardiac arrest reported'
        },
        {
            'id': 2,
            'emergency_id': 'EMS-2025-002',
            'severity': 'moderate',
            'status': 'en_route',
            'location': '37.7849,-122.4094',
            'reported_at': '2025-09-27T10:15:00Z',
            'description': 'Traffic accident with injuries'
        }
    ]
    return JsonResponse({
        'status': 'success',
        'count': len(sample_emergencies),
        'results': sample_emergencies
    })

@csrf_exempt
@require_http_methods(["POST"])
def create_emergency(request):
    """Create a new emergency"""
    return JsonResponse({'message': 'Create emergency endpoint - to be implemented'})

def emergency_detail(request, emergency_id):
    """Get emergency details"""
    return JsonResponse({'message': f'Emergency detail for {emergency_id} - to be implemented'})

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_emergency(request, emergency_id):
    """Update emergency status"""
    return JsonResponse({'message': f'Update emergency {emergency_id} - to be implemented'})

@csrf_exempt
@require_http_methods(["POST"])
def dispatch_ambulance(request, emergency_id):
    """Dispatch an ambulance to an emergency"""
    return JsonResponse({'message': f'Dispatch ambulance to emergency {emergency_id} - to be implemented'})

def emergency_types(request):
    """Get emergency types"""
    emergency_types = [
        {'id': 1, 'name': 'Cardiac Emergency', 'priority_level': 1, 'description': 'Heart-related emergencies'},
        {'id': 2, 'name': 'Trauma', 'priority_level': 1, 'description': 'Severe injuries from accidents'},
        {'id': 3, 'name': 'Respiratory Emergency', 'priority_level': 2, 'description': 'Breathing difficulties'},
        {'id': 4, 'name': 'Medical Emergency', 'priority_level': 3, 'description': 'General medical emergencies'},
    ]
    return JsonResponse({
        'status': 'success',
        'results': emergency_types
    })
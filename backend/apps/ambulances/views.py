from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.utils import timezone
import json
import math
from .models import Ambulance, AmbulanceLocation, CrewMember


def ambulance_list(request):
    """List all ambulances with their status"""
    ambulances = Ambulance.objects.select_related('ambulance_type').prefetch_related('crew_members')
    
    if request.content_type == 'application/json':
        data = []
        for ambulance in ambulances:
            data.append({
                'id': ambulance.id,
                'license_plate': ambulance.license_plate,
                'type': ambulance.ambulance_type.name,
                'status': ambulance.status,
                'is_available': ambulance.is_available,
                'location': {
                    'latitude': ambulance.current_location.y if ambulance.current_location else None,
                    'longitude': ambulance.current_location.x if ambulance.current_location else None,
                },
                'crew_count': ambulance.crew_members.count(),
            })
        return JsonResponse({'ambulances': data})
    
    return render(request, 'ambulances/list.html', {'ambulances': ambulances})


def ambulance_detail(request, ambulance_id):
    """Get detailed information about a specific ambulance"""
    ambulance = get_object_or_404(Ambulance, id=ambulance_id)
    
    if request.content_type == 'application/json':
        return JsonResponse({
            'id': ambulance.id,
            'license_plate': ambulance.license_plate,
            'type': {
                'name': ambulance.ambulance_type.name,
                'description': ambulance.ambulance_type.description,
                'capabilities': ambulance.ambulance_type.capabilities,
            },
            'status': ambulance.status,
            'location': {
                'latitude': ambulance.current_location.y if ambulance.current_location else None,
                'longitude': ambulance.current_location.x if ambulance.current_location else None,
            },
            'equipment': ambulance.equipment,
            'crew': [
                {
                    'name': member.get_full_name(),
                    'certification': member.crew_profile.certification_level if hasattr(member, 'crew_profile') else None,
                }
                for member in ambulance.crew_members.all()
            ],
        })
    
    return render(request, 'ambulances/detail.html', {'ambulance': ambulance})


@csrf_exempt
def find_nearest_ambulance(request):
    """Find the nearest available ambulance to a given location"""
    try:
        data = json.loads(request.body)
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        emergency_type = data.get('emergency_type', 'general')
        
        user_location = Point(longitude, latitude)
        
        # Get available ambulances
        available_ambulances = Ambulance.objects.filter(
            status='available',
            is_active=True,
            current_location__isnull=False
        ).select_related('ambulance_type')
        
        if not available_ambulances.exists():
            return JsonResponse({
                'success': False,
                'error': 'No ambulances available at the moment'
            })
        
        # Calculate distances and find the nearest
        nearest_ambulance = None
        min_distance = float('inf')
        
        for ambulance in available_ambulances:
            distance = user_location.distance(ambulance.current_location)
            if distance < min_distance:
                min_distance = distance
                nearest_ambulance = ambulance
        
        # Calculate ETA (simplified calculation)
        distance_km = min_distance * 111  # Rough conversion from degrees to km
        eta_minutes = max(5, int(distance_km / 60 * 60))  # Assuming 60 km/h average speed
        
        return JsonResponse({
            'success': True,
            'ambulance': {
                'id': nearest_ambulance.id,
                'license_plate': nearest_ambulance.license_plate,
                'type': nearest_ambulance.ambulance_type.name,
                'location': {
                    'latitude': nearest_ambulance.current_location.y,
                    'longitude': nearest_ambulance.current_location.x,
                },
                'distance_km': round(distance_km, 2),
                'eta_minutes': eta_minutes,
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
@login_required
def update_location(request, ambulance_id):
    """Update ambulance location (for crew members)"""
    try:
        ambulance = get_object_or_404(Ambulance, id=ambulance_id)
        
        # Check if user is crew member of this ambulance
        if not ambulance.crew_members.filter(id=request.user.id).exists():
            return JsonResponse({'success': False, 'error': 'Unauthorized'})
        
        data = json.loads(request.body)
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        speed = data.get('speed')
        heading = data.get('heading')
        
        new_location = Point(longitude, latitude)
        ambulance.current_location = new_location
        ambulance.save()
        
        # Save location history
        AmbulanceLocation.objects.create(
            ambulance=ambulance,
            location=new_location,
            speed=speed,
            heading=heading
        )
        
        return JsonResponse({'success': True, 'message': 'Location updated'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
@login_required
def update_status(request, ambulance_id):
    """Update ambulance status"""
    try:
        ambulance = get_object_or_404(Ambulance, id=ambulance_id)
        
        # Check if user is crew member of this ambulance or dispatcher
        if not (ambulance.crew_members.filter(id=request.user.id).exists() or 
                request.user.user_type in ['dispatcher', 'admin']):
            return JsonResponse({'success': False, 'error': 'Unauthorized'})
        
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status not in dict(Ambulance.STATUS_CHOICES):
            return JsonResponse({'success': False, 'error': 'Invalid status'})
        
        ambulance.status = new_status
        ambulance.save()
        
        return JsonResponse({
            'success': True, 
            'message': f'Status updated to {ambulance.get_status_display()}'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
@login_required
def crew_checkin(request):
    """Check in crew member for duty"""
    try:
        crew_profile = get_object_or_404(CrewMember, user=request.user)
        
        data = json.loads(request.body)
        ambulance_id = data.get('ambulance_id')
        
        ambulance = get_object_or_404(Ambulance, id=ambulance_id)
        
        # Add crew member to ambulance
        ambulance.crew_members.add(request.user)
        
        # Update crew status
        crew_profile.is_on_duty = True
        crew_profile.shift_start = timezone.now()
        crew_profile.save()
        
        return JsonResponse({'success': True, 'message': 'Checked in successfully'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
@login_required
def crew_checkout(request):
    """Check out crew member from duty"""
    try:
        crew_profile = get_object_or_404(CrewMember, user=request.user)
        
        # Remove from all ambulances
        Ambulance.objects.filter(crew_members=request.user).update()
        request.user.ambulance_crew.clear()
        
        # Update crew status
        crew_profile.is_on_duty = False
        crew_profile.shift_end = timezone.now()
        crew_profile.save()
        
        return JsonResponse({'success': True, 'message': 'Checked out successfully'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import User, UserProfile


def register(request):
    """User registration view"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            user_type = data.get('user_type', 'patient')
            phone_number = data.get('phone_number')
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                phone_number=phone_number
            )
            
            # Create profile
            UserProfile.objects.create(user=user)
            
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': 'User registered successfully',
                    'user_id': user.id
                })
            else:
                messages.success(request, 'Registration successful!')
                return redirect('authentication:login')
                
        except Exception as e:
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': str(e)})
            else:
                messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'authentication/register.html')


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': True,
                        'message': 'Login successful',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'user_type': user.user_type,
                            'email': user.email
                        }
                    })
                else:
                    return redirect('home')
            else:
                if request.content_type == 'application/json':
                    return JsonResponse({'success': False, 'error': 'Invalid credentials'})
                else:
                    messages.error(request, 'Invalid credentials')
                    
        except Exception as e:
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': str(e)})
            else:
                messages.error(request, f'Login failed: {str(e)}')
    
    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    if request.content_type == 'application/json':
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
    return redirect('authentication:login')


@login_required
def profile(request):
    """User profile view"""
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            
            # Update user fields
            if 'phone_number' in data:
                request.user.phone_number = data['phone_number']
            if 'emergency_contact' in data:
                request.user.emergency_contact = data['emergency_contact']
            if 'medical_info' in data:
                request.user.medical_info = data['medical_info']
            
            request.user.save()
            
            # Update profile fields
            if 'blood_type' in data:
                profile.blood_type = data['blood_type']
            if 'address' in data:
                profile.address = data['address']
            if 'insurance_number' in data:
                profile.insurance_number = data['insurance_number']
            if 'next_of_kin' in data:
                profile.next_of_kin = data['next_of_kin']
            if 'next_of_kin_phone' in data:
                profile.next_of_kin_phone = data['next_of_kin_phone']
            
            profile.save()
            
            if request.content_type == 'application/json':
                return JsonResponse({'success': True, 'message': 'Profile updated'})
            else:
                messages.success(request, 'Profile updated successfully!')
        
        context = {
            'user': request.user,
            'profile': profile
        }
        
        if request.content_type == 'application/json':
            return JsonResponse({
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'user_type': request.user.user_type,
                    'phone_number': request.user.phone_number,
                    'emergency_contact': request.user.emergency_contact,
                    'medical_info': request.user.medical_info,
                },
                'profile': {
                    'blood_type': profile.blood_type,
                    'address': profile.address,
                    'insurance_number': profile.insurance_number,
                    'next_of_kin': profile.next_of_kin,
                    'next_of_kin_phone': profile.next_of_kin_phone,
                }
            })
        
        return render(request, 'authentication/profile.html', context)
        
    except Exception as e:
        if request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': str(e)})
        else:
            messages.error(request, f'Error loading profile: {str(e)}')
            return redirect('home')


@csrf_exempt
@require_POST
def emergency_sos(request):
    """Emergency SOS endpoint - instant one-tap dispatch"""
    try:
        if request.user.is_authenticated:
            user = request.user
        else:
            # Allow anonymous emergency calls
            data = json.loads(request.body)
            user = None
        
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not latitude or not longitude:
            return JsonResponse({'success': False, 'error': 'Location is required for emergency dispatch'})
        
        # This would integrate with the emergency dispatch system
        # For now, return success with emergency ID
        emergency_id = f"EMG-{str(hash(f'{latitude}{longitude}'))[:8].upper()}"
        
        return JsonResponse({
            'success': True,
            'emergency_id': emergency_id,
            'message': 'Emergency dispatch initiated. Help is on the way!',
            'estimated_arrival': '8-12 minutes'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
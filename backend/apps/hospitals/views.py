from django.http import JsonResponse

def hospital_list(request):
    """Hospital list endpoint"""
    sample_hospitals = [
        {
            'id': 1,
            'name': 'City General Hospital',
            'hospital_type': 'general',
            'location': '37.7849,-122.4194',
            'emergency_services': True,
            'total_beds': 250,
            'available_beds': 15,
            'phone': '+1-555-0101'
        },
        {
            'id': 2,
            'name': 'Metro Trauma Center',
            'hospital_type': 'trauma',
            'location': '37.7949,-122.4094',
            'emergency_services': True,
            'total_beds': 180,
            'available_beds': 8,
            'phone': '+1-555-0102'
        }
    ]
    return JsonResponse({
        'status': 'success',
        'count': len(sample_hospitals),
        'results': sample_hospitals
    })
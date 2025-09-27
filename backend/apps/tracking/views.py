from django.http import JsonResponse

def tracking_list(request):
    """Tracking list endpoint"""
    return JsonResponse({'message': 'Tracking list endpoint - to be implemented'})
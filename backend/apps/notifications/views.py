from django.http import JsonResponse

def notification_list(request):
    """Notification list endpoint"""
    return JsonResponse({'message': 'Notification list endpoint - to be implemented'})
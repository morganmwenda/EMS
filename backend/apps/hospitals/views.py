from django.http import JsonResponse

def hospital_list(request):
    """Hospital list endpoint"""
    return JsonResponse({'message': 'Hospital list endpoint - to be implemented'})
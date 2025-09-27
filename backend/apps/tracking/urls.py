from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    # Placeholder URL patterns for tracking app
    path('', views.tracking_list, name='list'),
]
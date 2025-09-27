from django.urls import path
from . import views

app_name = 'ambulances'

urlpatterns = [
    path('', views.ambulance_list, name='list'),
    path('<int:ambulance_id>/', views.ambulance_detail, name='detail'),
    path('nearest/', views.find_nearest_ambulance, name='nearest'),
    path('<int:ambulance_id>/location/', views.update_location, name='update_location'),
    path('<int:ambulance_id>/status/', views.update_status, name='update_status'),
    path('crew/checkin/', views.crew_checkin, name='crew_checkin'),
    path('crew/checkout/', views.crew_checkout, name='crew_checkout'),
]
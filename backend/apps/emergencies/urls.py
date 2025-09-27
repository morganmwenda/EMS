from django.urls import path
from . import views

app_name = 'emergencies'

urlpatterns = [
    path('', views.emergency_list, name='list'),
    path('create/', views.create_emergency, name='create'),
    path('<str:emergency_id>/', views.emergency_detail, name='detail'),
    path('<str:emergency_id>/update/', views.update_emergency, name='update'),
    path('<str:emergency_id>/dispatch/', views.dispatch_ambulance, name='dispatch'),
    path('types/', views.emergency_types, name='types'),
]
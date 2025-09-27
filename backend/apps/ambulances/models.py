from django.db import models
from django.contrib.gis.db import models as gis_models
from apps.authentication.models import User


class AmbulanceType(models.Model):
    """Types of ambulances with different capabilities"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    capabilities = models.JSONField(default=list, help_text="List of medical capabilities")
    
    def __str__(self):
        return self.name


class Ambulance(models.Model):
    """Ambulance model with location and status tracking"""
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('dispatched', 'Dispatched'),
        ('en_route', 'En Route'),
        ('on_scene', 'On Scene'),
        ('transporting', 'Transporting'),
        ('at_hospital', 'At Hospital'),
        ('maintenance', 'Maintenance'),
        ('off_duty', 'Off Duty'),
    )
    
    license_plate = models.CharField(max_length=20, unique=True)
    ambulance_type = models.ForeignKey(AmbulanceType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    current_location = gis_models.PointField(help_text="Current GPS location")
    base_station = gis_models.PointField(help_text="Home base location")
    crew_members = models.ManyToManyField(User, related_name='ambulance_crew', blank=True)
    equipment = models.JSONField(default=list, help_text="Available medical equipment")
    last_maintenance = models.DateTimeField(blank=True, null=True)
    next_maintenance = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['license_plate']
    
    def __str__(self):
        return f"Ambulance {self.license_plate} ({self.get_status_display()})"
    
    @property
    def is_available(self):
        return self.status == 'available' and self.is_active


class AmbulanceLocation(models.Model):
    """Historical location tracking for ambulances"""
    ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE, related_name='location_history')
    location = gis_models.PointField()
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.FloatField(blank=True, null=True, help_text="Speed in km/h")
    heading = models.FloatField(blank=True, null=True, help_text="Direction in degrees")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.ambulance.license_plate} at {self.timestamp}"


class CrewMember(models.Model):
    """Extended information for ambulance crew members"""
    
    CERTIFICATION_LEVELS = (
        ('emt_basic', 'EMT Basic'),
        ('emt_intermediate', 'EMT Intermediate'),
        ('emt_paramedic', 'EMT Paramedic'),
        ('nurse', 'Registered Nurse'),
        ('doctor', 'Doctor'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='crew_profile')
    certification_level = models.CharField(max_length=20, choices=CERTIFICATION_LEVELS)
    license_number = models.CharField(max_length=50)
    license_expiry = models.DateField()
    specializations = models.JSONField(default=list, help_text="Medical specializations")
    is_on_duty = models.BooleanField(default=False)
    shift_start = models.DateTimeField(blank=True, null=True)
    shift_end = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_certification_level_display()})"
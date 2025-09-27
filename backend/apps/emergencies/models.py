from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils import timezone
from apps.authentication.models import User
from apps.ambulances.models import Ambulance
from apps.hospitals.models import Hospital


class EmergencyType(models.Model):
    """Types of emergencies with priority levels"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    priority_level = models.IntegerField(choices=(
        (1, 'Critical'),
        (2, 'High'),
        (3, 'Medium'),
        (4, 'Low'),
    ), default=3)
    required_equipment = models.JSONField(default=list)
    estimated_response_time = models.IntegerField(help_text="Minutes")
    
    class Meta:
        ordering = ['priority_level', 'name']
    
    def __str__(self):
        return f"{self.name} (Priority {self.priority_level})"


class Emergency(models.Model):
    """Emergency incident model"""
    
    STATUS_CHOICES = (
        ('reported', 'Reported'),
        ('dispatched', 'Dispatched'),
        ('en_route', 'En Route'),
        ('on_scene', 'On Scene'),
        ('transporting', 'Transporting'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    SEVERITY_CHOICES = (
        ('critical', 'Critical'),
        ('serious', 'Serious'),
        ('moderate', 'Moderate'),
        ('minor', 'Minor'),
    )
    
    emergency_id = models.CharField(max_length=20, unique=True)
    caller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_calls')
    caller_phone = models.CharField(max_length=20, help_text="For anonymous calls")
    emergency_type = models.ForeignKey(EmergencyType, on_delete=models.CASCADE)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='moderate')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    
    # Location information
    location = gis_models.PointField(help_text="Emergency location")
    address = models.TextField(blank=True, null=True)
    landmark = models.CharField(max_length=200, blank=True, null=True)
    
    # Patient information
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    patient_age = models.IntegerField(blank=True, null=True)
    patient_gender = models.CharField(max_length=10, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ), blank=True, null=True)
    patient_condition = models.TextField(blank=True, null=True)
    
    # Response information
    assigned_ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    dispatcher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatched_emergencies')
    
    # Timing
    reported_at = models.DateTimeField(auto_now_add=True)
    dispatched_at = models.DateTimeField(blank=True, null=True)
    arrived_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Additional information
    description = models.TextField()
    notes = models.TextField(blank=True, null=True)
    priority_score = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-reported_at']
    
    def __str__(self):
        return f"Emergency {self.emergency_id} - {self.emergency_type.name}"
    
    def save(self, *args, **kwargs):
        if not self.emergency_id:
            # Generate unique emergency ID
            import uuid
            self.emergency_id = f"EMG-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def response_time(self):
        """Calculate response time in minutes"""
        if self.dispatched_at and self.arrived_at:
            return (self.arrived_at - self.dispatched_at).total_seconds() / 60
        return None
    
    @property
    def total_time(self):
        """Calculate total time from report to completion"""
        if self.completed_at:
            return (self.completed_at - self.reported_at).total_seconds() / 60
        return None


class EmergencyUpdate(models.Model):
    """Status updates and notes for emergencies"""
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE, related_name='updates')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Emergency.STATUS_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Update for {self.emergency.emergency_id} at {self.timestamp}"


class EmergencyCall(models.Model):
    """Voice/video call records for emergencies"""
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE, related_name='calls')
    caller = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_calls')
    call_type = models.CharField(max_length=10, choices=(
        ('voice', 'Voice'),
        ('video', 'Video'),
    ))
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True, help_text="Duration in seconds")
    
    def __str__(self):
        return f"{self.call_type.title()} call for {self.emergency.emergency_id}"
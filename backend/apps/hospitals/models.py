from django.db import models
from django.contrib.gis.db import models as gis_models


class Hospital(models.Model):
    """Hospital model with location and capacity information"""
    
    HOSPITAL_TYPES = (
        ('general', 'General Hospital'),
        ('trauma', 'Trauma Center'),
        ('specialty', 'Specialty Hospital'),
        ('clinic', 'Clinic'),
        ('emergency', 'Emergency Room'),
    )
    
    name = models.CharField(max_length=200)
    hospital_type = models.CharField(max_length=20, choices=HOSPITAL_TYPES, default='general')
    address = models.TextField()
    location = gis_models.PointField(help_text="Hospital GPS location")
    phone_number = models.CharField(max_length=20)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Capacity information
    total_beds = models.IntegerField(default=0)
    emergency_beds = models.IntegerField(default=0)
    icu_beds = models.IntegerField(default=0)
    available_beds = models.IntegerField(default=0)
    
    # Services and specialties
    services = models.JSONField(default=list, help_text="List of medical services")
    specialties = models.JSONField(default=list, help_text="Medical specialties")
    emergency_services = models.BooleanField(default=True)
    trauma_center_level = models.IntegerField(blank=True, null=True, choices=(
        (1, 'Level I'),
        (2, 'Level II'),
        (3, 'Level III'),
        (4, 'Level IV'),
    ))
    
    # Operating hours
    is_24_7 = models.BooleanField(default=True)
    operating_hours = models.JSONField(default=dict, help_text="Operating hours by day")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def occupancy_rate(self):
        """Calculate bed occupancy rate"""
        if self.total_beds > 0:
            occupied = self.total_beds - self.available_beds
            return (occupied / self.total_beds) * 100
        return 0

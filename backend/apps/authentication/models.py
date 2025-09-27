from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.gis.db import models as gis_models  # Commented out for now - add GIS support later


class User(AbstractUser):
    """Extended User model for EMS system"""
    
    USER_TYPES = (
        ('patient', 'Patient'),
        ('dispatcher', 'Dispatcher'),
        ('ambulance_crew', 'Ambulance Crew'),
        ('hospital_staff', 'Hospital Staff'),
        ('admin', 'System Admin'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='patient')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    medical_info = models.TextField(blank=True, null=True, help_text="Allergies, medications, conditions")
    is_verified = models.BooleanField(default=False)
    # location = gis_models.PointField(blank=True, null=True)  # TODO: Enable when GIS support is added
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Temporary text field - will be PointField when GIS is enabled")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'auth_user'
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class UserProfile(models.Model):
    """Additional profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)
    next_of_kin = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
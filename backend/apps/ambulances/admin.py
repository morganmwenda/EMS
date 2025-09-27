from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import AmbulanceType, Ambulance, AmbulanceLocation, CrewMember


@admin.register(AmbulanceType)
class AmbulanceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Ambulance)
class AmbulanceAdmin(OSMGeoAdmin):
    list_display = ('license_plate', 'ambulance_type', 'status', 'is_active', 'updated_at')
    list_filter = ('status', 'is_active', 'ambulance_type')
    search_fields = ('license_plate',)
    filter_horizontal = ('crew_members',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('license_plate', 'ambulance_type', 'status', 'is_active')
        }),
        ('Location', {
            'fields': ('current_location', 'base_station')
        }),
        ('Crew & Equipment', {
            'fields': ('crew_members', 'equipment')
        }),
        ('Maintenance', {
            'fields': ('last_maintenance', 'next_maintenance')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AmbulanceLocation)
class AmbulanceLocationAdmin(admin.ModelAdmin):
    list_display = ('ambulance', 'timestamp', 'speed', 'heading')
    list_filter = ('ambulance', 'timestamp')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'certification_level', 'is_on_duty', 'license_expiry')
    list_filter = ('certification_level', 'is_on_duty')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number')
    readonly_fields = ('user',)
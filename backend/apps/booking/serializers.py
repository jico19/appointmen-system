from rest_framework import serializers
from . import models





class AppointmentSerializers(serializers.ModelSerializer):
    
    # updated_at = serializers.SerializerMethodField()
    # date = serializers.SerializerMethodField()
    assigned_staff_name = serializers.CharField(
        source = 'assigned_staff.username', read_only = True
    )
    user_name = serializers.CharField(
        source = 'user.username', read_only=True
    )
    
    
    class Meta:
        model = models.Appointment
        fields = "__all__"
        extra_kwagrs = {
            'date': { 'write_only': True }
        }
        
    # def get_updated_at(self, obj):
    #     return obj.updated_at.strftime('%B %d, %Y %I:%M %p')
    
    # def get_date(self, obj):
    #     return obj.date.strftime('%B %d, %Y %I:%M %p')

class RepairLogSerializer(serializers.ModelSerializer):
    
    recorded_by = serializers.CharField(
        source = 'recorded_by.username', read_only = True
    )
    
    class Meta:
        model = models.RepairLog
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Notification
        fields = "__all__"

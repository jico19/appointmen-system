from rest_framework import viewsets, response, status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from . import serializers
from . import models

class AppointmentViewSets(viewsets.ModelViewSet):
    queryset = models.Appointment.objects.all()
    serializer_class = serializers.AppointmentSerializers
    
    
    @action(detail=True, methods=['POST'])
    def accept(self, request, pk = None):
        try:
            object = get_object_or_404(
                models.Appointment, id = pk
            )
            
            if object.status == models.Appointment.StatusChoice.ACCEPTED:
                return response.Response("Already Accepted try another one", status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():        
                # step 1
                object.status = models.Appointment.StatusChoice.ACCEPTED
                object.assigned_staff = request.user
                # step 2 create repair log
                models.RepairLog.objects.create(
                    appointment_id = object.id,
                    recorded_by = request.user
                )
            
                # step 3 notify
                models.Notification.objects.create(
                    title = "You appointment has been accepted. please wait for further updates.",
                    recipient = object.user
                )
                object.save()
            
            return response.Response("accepted!", status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return response.Response("Something went wrong while performing this action", status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['POST'])
    def reject(self, request, pk = None):
        """
            Reject Endpoint for appointment
        """
        try:
            with transaction.atomic():
                data = request.data
                
                object = get_object_or_404(
                    models.Appointment, id = pk
                )
                
                object.status = models.Appointment.StatusChoice.REJECTED
                object.rejection_reason = data.get('rejection_reason')
                models.Notification.objects.create(
                    title = "You appointment has been rejected.",
                    recipient = object.user
                )
                object.save()
                
                return response.Response("rejected", status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return response.Response("Something went wrong while performing this action", status=status.HTTP_400_BAD_REQUEST)



class RepairLogViewSets(viewsets.ModelViewSet):
    queryset = models.RepairLog.objects.all()
    serializer_class = serializers.RepairLogSerializer
    
class NotificationViewSets(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    
    
    
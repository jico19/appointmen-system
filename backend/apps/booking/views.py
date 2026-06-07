from rest_framework import viewsets, response, status
from rest_framework.decorators import action
from .services import AppointmentService
from django.db import transaction
from . import serializers
from . import models

class AppointmentViewSets(viewsets.ModelViewSet):
    queryset = models.Appointment.objects.all()
    serializer_class = serializers.AppointmentSerializers
    
    
    @action(detail=True, methods=['POST'])
    def accept(self, request, pk = None):
        try:
            with transaction.atomic():
                appointment = (
                    models.Appointment.objects
                    .select_for_update()
                    .get(id=pk)
                )
                AppointmentService.accept(self=appointment, staff=request.user)
                
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
                
                # step 1
                appointment = (
                    models.Appointment.objects
                    .select_for_update()
                    .get(id=pk)
                )
                    
                AppointmentService.reject(
                    self=appointment,
                    staff=request.user,
                    rejection_reason=data.get("rejection_reason")
                )
                
                return response.Response("rejected", status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return response.Response("Something went wrong while performing this action", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def receive(self, request, pk = None):
        with transaction.atomic():
            appointment = (
                models.Appointment.objects
                .select_for_update()
                .get(id=pk)
            )
            AppointmentService.receive(self=appointment)
            return response.Response("the item has been received")
        
    @action(detail=True, methods=['POST'])
    def diagnose(self, request, pk = None):
        with transaction.atomic():
            data = request.data
            
            appointment = (
                models.Appointment.objects
                .select_for_update()
                .get(id=pk)
            )
            
            AppointmentService.diagnose(
                self=appointment,
                findings=data.get('findings', '')
            )
            
            return response.Response("Item Diagnostic sucess", status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['POST'])
    def repair(self, request, pk = None):
        with transaction.atomic():
            data = request.data
            
            appointment = (
                models.Appointment
                .objects
                .select_for_update()
                .get(id = pk)
            )
            
            AppointmentService.repair(
                self=appointment,
                data=data
            )
            
        return response.Response("Repair", status=status.HTTP_200_OK)
    
    
class RepairLogViewSets(viewsets.ModelViewSet):
    queryset = models.RepairLog.objects.all()
    serializer_class = serializers.RepairLogSerializer
    
class NotificationViewSets(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    
    
    
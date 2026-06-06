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
            with transaction.atomic():      
                appointment = (
                    models.Appointment.objects
                    .select_for_update()
                    .get(id=pk)
                )
                        
                if appointment.status == models.Appointment.StatusChoice.ACCEPTED:
                    return response.Response("Already Accepted try another one", status=status.HTTP_400_BAD_REQUEST)  
                # step 1
                appointment.status = models.Appointment.StatusChoice.ACCEPTED
                appointment.assigned_staff = request.user
                appointment.save()
                
                # step 2 create repair log
                models.RepairLog.objects.create(
                    appointment_id = object.id,
                    recorded_by = request.user
                )
                # step 3 notify
                models.Notification.objects.create(
                    title = "You appointment has been accepted. please wait for further updates.",
                    recipient = appointment.user
                )
            
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
                    
                appointment.status = models.Appointment.StatusChoice.REJECTED
                appointment.rejection_reason = data.get('rejection_reason')
                appointment.save()
                # step 2
                models.Notification.objects.create(
                    title = "You appointment has been rejected.",
                    recipient = appointment.user
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
            
            if appointment.status == models.Appointment.StatusChoice.RECEIVE:
                return response.Response("This appointment is already received.", status=status.HTTP_400_BAD_REQUEST)
            
            appointment.status = models.Appointment.StatusChoice.RECEIVE
            appointment.save()
            
            models.Notification.objects.create(
                    title = "Your Item has been received in the repair shop.",
                    recipient = object.user
                )
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
            
            repair_logs = appointment.logs
            
            if appointment.status == models.Appointment.StatusChoice.DIAGNOSING:
                return response.Response("This appointment is already under diagnosing.", status=status.HTTP_400_BAD_REQUEST) 
            
            appointment.status = models.Appointment.StatusChoice.DIAGNOSING
            appointment.save()
            repair_logs.findings = data.get("findings")
            repair_logs.save()
            
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
            repair_logs = appointment.logs
            
            if appointment.status == models.Appointment.StatusChoice.REPAIRING:
                return response.Response("This appointment is already under repairing.", status=status.HTTP_400_BAD_REQUEST) 
            
            appointment.status = models.Appointment.StatusChoice.REPAIRING
            appointment.save()
            
            repair_logs.remarks = data.get('remarks')
            repair_logs.qouted_amount = data.get('qouted_amount')
            repair_logs.status_at_time = data.get('status_at_time')
            repair_logs.save()
            
        return response.Response("Repair", status=status.HTTP_200_OK)
    
    
class RepairLogViewSets(viewsets.ModelViewSet):
    queryset = models.RepairLog.objects.all()
    serializer_class = serializers.RepairLogSerializer
    
class NotificationViewSets(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    
    
    
from . import models
from django.core.exceptions import ValidationError


class Notification:
    
    @staticmethod
    def send_notif(title, recipient):
        models.Notification.objects.create(
            title = title,
            recipient = recipient
        )


class AppointmentService:
    
    def accept(self, staff):
        
        if self.status == models.Appointment.StatusChoice.ACCEPTED:
            raise ValidationError("Invalid Status.")

        self.assigned_staff = staff
        self.save()
        
        models.RepairLog.objects.create(
            appointment_id = self.id,
            recorded_by = staff
        )
        
        Notification.send_notif(
            title="You appointment has been accepted. please wait for further updates.",
            recipient= staff
        )
        
        
    def reject(self, staff, rejection_reason):
        
        if self.status == models.Appointment.StatusChoice.REJECTED:
            raise ValidationError("Invalid Status.")
        
        self.status = models.Appointment.StatusChoice.REJECTED
        self.rejection_reason = rejection_reason
        self.save()
        
        Notification.send_notif(
            title="You appointment has been rejected.",
            recipient=staff
        )
        
    def receive(self):
        if self.status == models.Appointment.StatusChoice.RECEIVE:
            raise ValidationError("Invalid Status.")
        
        self.status = models.Appointment.StatusChoice.RECEIVE
        self.save()
        
        Notification.send_notif(
            title="Your Item has been received in the repair shop.",
            recipient=self.user
        )
        
    def diagnose(self, findings):
        if self.status == models.Appointment.StatusChoice.DIAGNOSING:
            raise ValidationError("Invalid Status.")
        
        repair_log = self.logs
        
        self.status = models.Appointment.StatusChoice.DIAGNOSING
        self.save()
        repair_log.findings = findings
        repair_log.save()
        
        Notification.send_notif(
            title="Your item is under diagnostic.",
            recipient=self.user
        )
        
    def repair(self, data):        
        if self.status == models.Appointment.StatusChoice.REPAIRING:
            raise ValidationError("Invalid Status.")
        
        repair_log = self.logs
        
        self.status = models.Appointment.StatusChoice.REPAIRING
        self.save()
        
        repair_log.remarks = data.get("remarks", "")
        repair_log.qouted_amount = data.get("qouted_amount", "")
        repair_log.status_at_time = data.get("status_at_time", "")
        repair_log.save()
        
        Notification.send_notif(
            title="Your item has been repair and ready for pickup.",
            recipient=self.user
        )
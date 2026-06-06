from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save,sender=models.Appointment)
def update_status_pickup(sender, instance, created, **kwargs):
    
    if instance.status == models.Appointment.StatusChoice.REPAIRING:
        instance.status = models.Appointment.StatusChoice.PICKUP
        instance.save()
        
        models.Notification(
            title = f"Your item is ready for pickup overall amount is :{instance.logs.quoted_amount}",
            recipient = instance.user
        )

from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.Appointment)
def update_status_pickup(sender, instance, created, **kwargs):
    if kwargs.get('raw'):
        return

    if instance.status == models.Appointment.StatusChoice.REPAIRING:
        instance.status = models.Appointment.StatusChoice.PICKUP
        instance.save()

        quoted_amount = instance.logs.quoted_amount if hasattr(
            instance, 'logs') else 0.00

        models.Notification.objects.create(
            title=f"Your item is ready for pickup overall amount is :{quoted_amount}",
            recipient=instance.user
        )

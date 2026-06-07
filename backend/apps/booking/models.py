from django.db import models
import uuid
from apps.core.models import User
from django.core.exceptions import ValidationError


class Appointment(models.Model):

    class ServiceChoice(models.TextChoices):
        CLEANING = "CLEANING", "Cleaning"
        REPAIR = "REPAIR", "Repair"
        HOME_SERVICE = "HOME_SERVICES", "Home Services"

    class StatusChoice(models.TextChoices):
        PENDING = "PENDING", "Pending"  # just booked, awaiting staff review
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"  # staff declined
        RECEIVE = "RECEIVE", "Item has been received"
        DIAGNOSING = "DIAGNOSING", "Diagnosing the problem"
        REPAIRING = "REPAIRING", "Repairing the problem"
        PICKUP = "PICKUP", "Ready for pickup"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentStatus(models.TextChoices):
        PAID = "PAID", "Paid"
        PAYMENT_PENDING = "PAYMENT_PENDING", "Payment Pending"
        PARTIAL = "PARTIAL", "Partial"  # Downpayment

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    service = models.CharField(max_length=100, choices=ServiceChoice)
    address = models.TextField(blank=True)
    issue = models.TextField()

    payment_status = models.CharField(
        max_length=50, choices=PaymentStatus, default=PaymentStatus.PAYMENT_PENDING
    )

    # staff actions
    assigned_staff = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff"
    )
    status = models.CharField(
        max_length=50, choices=StatusChoice, default=StatusChoice.PENDING
    )
    rejection_reason = models.TextField(blank=True)

    date = models.DateTimeField(null=True, help_text="the appointment date")
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Appointment #{self.id} {self.service} | {self.date.strftime('%B %d, %Y %I:%M %p')}"

    class Meta:
        ordering = ["-date"]


class RepairLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name="logs", editable=False
    )
    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assigned"
    )

    device_type = models.CharField(
        max_length=100, help_text="e.g. Laptop, Desktop, Phone", blank=True
    )
    findings = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status_at_time = models.CharField(
        max_length=30, help_text="Snapshot of appointment status when logged"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Log for {self.appointment} by {self.recorded_by}"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.title} to {self.recipient.username or self.recipient.get_full_name()}"

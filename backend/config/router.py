from rest_framework import routers
from apps.booking import views as BookingViewSets


router = routers.DefaultRouter()

router.register(r'appointment', BookingViewSets.AppointmentViewSets)
router.register(r'repair-logs', BookingViewSets.RepairLogViewSets)
router.register(r'notification', BookingViewSets.NotificationViewSets)
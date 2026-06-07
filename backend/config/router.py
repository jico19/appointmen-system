from rest_framework import routers
from apps.booking import views as BookingViewSets
from apps.core import views as CoreViewSets

router = routers.DefaultRouter()

router.register(r'user', CoreViewSets.UserViewSets)
router.register(r'appointment', BookingViewSets.AppointmentViewSets)
router.register(r'repair-logs', BookingViewSets.RepairLogViewSets)
router.register(r'notification', BookingViewSets.NotificationViewSets)
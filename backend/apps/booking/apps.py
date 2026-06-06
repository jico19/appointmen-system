from django.apps import AppConfig


class BookingConfig(AppConfig):
    name = 'apps.booking'

    def ready(self):
        import apps.booking.signals
from .delivery_command import DeliveryCommand
from datetime import datetime, timedelta
from django.utils import timezone

class AddDeliveryCommand(DeliveryCommand):
    def __init__(self, geocoding_service, delivery_repository, delivery_factory):
        self.geocoding_service = geocoding_service
        self.delivery_repository = delivery_repository
        self.delivery_factory = delivery_factory

    def execute(self, **kwargs):
        address = kwargs.get("address")
        delivery_type = kwargs.get("delivery_type", "normal")

        latitude, longitude = self.geocoding_service.get_coordinates(address)

        delivery = self.delivery_factory.create_delivery(
            delivery_type=delivery_type,
            address=address,
            latitude=latitude,
            longitude=longitude,
            scheduled_time=kwargs.get("scheduled_time", timezone.now() + timedelta(hours=1)),        
            priority_level=kwargs.get("priority_level", 3)
        )

        return self.delivery_repository.add_or_update_delivery(delivery)
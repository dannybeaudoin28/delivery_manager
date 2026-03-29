from .delivery_command import DeliveryCommand
from datetime import datetime, timedelta
from django.utils import timezone

class AddDeliveryCommand(DeliveryCommand):
    # Constructor initializes required dependencies:
    # - geocoding_service: converts address into coordinates
    # - delivery_repository: handles database operations
    # - delivery_factory: creates delivery objects
    def __init__(self, geocoding_service, delivery_repository, delivery_factory):
        self.geocoding_service = geocoding_service
        self.delivery_repository = delivery_repository
        self.delivery_factory = delivery_factory

    # Executes the command to create and store a new delivery
    def execute(self, **kwargs):
        # Extract address from input arguments
        address = kwargs.get("address")

        # Get delivery type (default is "normal" if not provided)
        delivery_type = kwargs.get("delivery_type", "normal")

        # Convert address into latitude and longitude using geocoding service
        latitude, longitude = self.geocoding_service.get_coordinates(address)

        # Create a new delivery object using the factory
        delivery = self.delivery_factory.create_delivery(
            delivery_type=delivery_type,
            address=address,
            latitude=latitude,
            longitude=longitude,

            # Use provided scheduled_time or default to 1 hour from now
            scheduled_time=kwargs.get(
                "scheduled_time",
                timezone.now() + timedelta(hours=1)
            ),

            # Use provided priority level or default to 3
            priority_level=kwargs.get("priority_level", 3)
        )

        # Save the delivery to the database (or update if it already exists)
        return self.delivery_repository.add_or_update_delivery(delivery)
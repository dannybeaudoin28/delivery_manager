from .delivery_command import DeliveryCommand

class AddDeliveryCommand(DeliveryCommand):
    def __init__(self, geocoding_service, delivery_repository, delivery_factory):
        self.geocoding_service = geocoding_service
        self.delivery_repository = delivery_repository
        self.delivery_factory = delivery_factory

    def execute(self, kwargs):
        address, delivery_type = kwargs
        latitude, longitude = self.geocoding_service.get_coordinates(address)

        delivery = self.delivery_factory.create_delivery(
            delivery_type=delivery_type,
            address=address,
            latitude=latitude,
            longitude=longitude,
        )

        return self.delivery_repository.add_or_update_delivery(delivery)
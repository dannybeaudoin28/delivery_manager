from .delivery_command import DeliveryCommand
from deliverymanager.models import Delivery


class AddDeliveryCommand(DeliveryCommand):

    def execute(self, address):
        latitude, longitude = self.geocoding_service.get_coordinates(address)

        delivery = Delivery(
            address=address,
            latitude=latitude,
            longitude=longitude
        )

        return self.delivery_repository.add_or_update_delivery(delivery)
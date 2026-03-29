from deliverymanager.commands.delivery_command import DeliveryCommand


class UpdateDeliveryCommand(DeliveryCommand):
    """
    Command responsible for updating an existing delivery.
    Encapsulates business rules for delivery edits.
    """

    def __init__(self, delivery_repository, geocoding_service):
        self.delivery_repository = delivery_repository
        self.geocoding_service = geocoding_service

    def execute(self, delivery_id, **kwargs):
        """
        Update a delivery.

        Supported fields:
            - address

        If the address changes, the delivery is re-geocoded so latitude
        and longitude remain consistent with the stored address.

        Args:
            delivery_id (int): The ID of the delivery to update.
            **kwargs: Fields to update.

        Returns:
            Delivery: The updated delivery instance.
        """
        delivery = self.delivery_repository.get_delivery_by_id(delivery_id)

        new_address = kwargs.get("address", "").strip()

        if new_address and new_address != delivery.address:
            latitude, longitude = self.geocoding_service.get_coordinates(new_address)
            delivery.address = new_address
            delivery.latitude = latitude
            delivery.longitude = longitude

        return self.delivery_repository.add_or_update_delivery(delivery)
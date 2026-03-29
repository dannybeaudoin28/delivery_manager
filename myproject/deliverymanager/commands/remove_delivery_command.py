from deliverymanager.commands.delivery_command import DeliveryCommand

class RemoveDeliveryCommand(DeliveryCommand):
    """
    Command responsible for removing an existing delivery.
    Encapsulates the delete use case so views remain thin.
    """

    def __init__(self, delivery_repository):
        self.delivery_repository = delivery_repository

    def execute(self, delivery_id):
        """
        Remove a delivery by its ID.

        Args:
            delivery_id (int): The ID of the delivery to remove.

        Returns:
            int: Number of deleted rows.
        """
        delivery = self.delivery_repository.get_delivery_by_id(delivery_id)
        return self.delivery_repository.remove_delivery(delivery)
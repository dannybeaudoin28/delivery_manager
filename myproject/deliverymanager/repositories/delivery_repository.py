from deliverymanager.models import Delivery


class DeliveryRepository:
    """
    Repository responsible for data access related to Delivery objects.
    Keeps ORM usage centralized so views and commands stay focused on
    application behavior rather than persistence details.
    """

    def add_or_update_delivery(self, delivery):
        """
        Save a delivery instance.

        Args:
            delivery (Delivery): The delivery to persist.

        Returns:
            Delivery: The saved delivery instance.
        """
        delivery.save()
        return delivery

    def get_delivery_by_id(self, delivery_id):
        """
        Retrieve a delivery by its primary key.

        Args:
            delivery_id (int): Delivery ID.

        Returns:
            Delivery: Matching delivery instance.
        """
        return Delivery.objects.get(id=delivery_id)

    def get_unassigned_deliveries(self):
        """
        Retrieve all unassigned deliveries.

        Returns:
            QuerySet[Delivery]: Unassigned deliveries.
        """
        return Delivery.objects.filter(
            status=Delivery.STATUS_UNASSIGNED
        ).order_by("created_at")

    def get_all_deliveries(self):
        """
        Retrieve all deliveries in reverse creation order.

        Returns:
            QuerySet[Delivery]: All deliveries.
        """
        return Delivery.objects.all().order_by("-created_at")

    def get_deliveries_for_route(self, route):
        """
        Retrieve all deliveries associated with a route.

        Args:
            route (Route): Route instance.

        Returns:
            QuerySet[Delivery]: Deliveries assigned to the route.
        """
        return Delivery.objects.filter(route=route)

    def remove_delivery(self, delivery):
        """
        Delete a delivery instance.

        Args:
            delivery (Delivery): Delivery to delete.

        Returns:
            tuple[int, dict]: Django delete result.
        """
        return delivery.delete()

    def clear_queue(self):
        """
        Delete all currently unassigned deliveries.

        Returns:
            int: Number of deleted rows.
        """
        deleted_count, _ = Delivery.objects.filter(
            status=Delivery.STATUS_UNASSIGNED
        ).delete()
        return deleted_count

    def mark_delivered(self, delivery):
        """
        Mark a delivery as delivered and clear route-specific metadata.

        Args:
            delivery (Delivery): Delivery to update.

        Returns:
            Delivery: Updated delivery instance.
        """
        delivery.status = Delivery.STATUS_DELIVERED
        delivery.route = None
        delivery.route_order = None
        delivery.leg_distance_meters = None
        delivery.leg_duration_seconds = None
        delivery.save()
        return delivery
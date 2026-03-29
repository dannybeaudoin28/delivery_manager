from ..models import Delivery, CustomDelivery
from datetime import datetime, timedelta


class DeliveryFactory:
    """
    Factory responsible for creating Delivery objects.

    Encapsulates object creation logic and allows the system to decide
    at runtime whether to create a standard Delivery or a CustomDelivery.
    """

    @staticmethod
    def create_delivery(delivery_type, address, latitude=None, longitude=None, **kwargs):
        """
        Create a delivery instance based on the specified type.

        Args:
            delivery_type (str): Type of delivery ("normal" or "custom").
            address (str): Delivery address.
            latitude (float, optional): Latitude of the address.
            longitude (float, optional): Longitude of the address.
            **kwargs: Additional fields for custom deliveries
                      (e.g., scheduled_time, priority_level).

        Returns:
            Delivery | CustomDelivery: Newly created delivery instance (not yet saved).
        """
        if delivery_type == "custom":
            # Create a custom delivery with optional scheduling and priority
            return CustomDelivery(
                address=address,
                latitude=latitude,
                longitude=longitude,
                is_custom=True,
                status="Unassigned",
                scheduled_time=kwargs.get("scheduled_time", datetime.now() + timedelta(hours=1)),
                priority_level=kwargs.get("priority_level", 3)
            )
        else:
            # Create a standard delivery with default status
            return Delivery(
                address=address,
                latitude=latitude,
                longitude=longitude,
                status="Unassigned"
            )
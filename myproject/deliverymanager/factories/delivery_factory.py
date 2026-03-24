from ..models import Delivery, CustomDelivery
from datetime import datetime, timedelta

class DeliveryFactory:
    @staticmethod
    def create_delivery(delivery_type, address, latitude=None, longitude=None, **kwargs):
        if delivery_type == "custom":
            print("Custom delivery object created")
            return CustomDelivery(
                address=address,
                latitude=latitude,
                longitude=longitude,
                status="Unassigned",
                scheduled_time=kwargs.get("scheduled_time", datetime.now() + timedelta(hours=1)),
                priority_level=kwargs.get("priority_level", 3)
            )
        else:
            print("Normal delivery created")
            return Delivery(
                address=address,
                latitude=latitude,
                longitude=longitude,
                status="Unassigned"
            )
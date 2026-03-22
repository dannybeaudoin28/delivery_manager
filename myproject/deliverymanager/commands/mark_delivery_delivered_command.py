from deliverymanager.models import Delivery, Driver
from deliverymanager.repositories.delivery_repository import DeliveryRepository



class MarkDeliveryDeliveredCommand:
    def __init__(self, delivery_repository):
        self.delivery_repository = delivery_repository

    def execute(self, id):
        print("Inside command id is: " + str(id))
        delivery = self.delivery_repository.get_delivery_by_id(id)
        route = delivery.route

        self.delivery_repository.mark_delivered(delivery)

        if route is not None:
            remaining = route.deliveries.filter(status=Delivery.STATUS_ASSIGNED).count()

            if remaining == 0:
                driver = Driver.objects.filter(route=route).first()
                if driver:
                    driver.route = None
                    driver.save()

        return delivery
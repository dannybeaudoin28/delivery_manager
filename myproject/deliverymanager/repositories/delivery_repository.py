from deliverymanager.models import Delivery

class DeliveryRepository:
    
    def add_or_update_delivery(self, delivery):
        delivery.save()
        return delivery

    def remove_delivery(self, delivery_id):
        deleted_count, _ = Delivery.objects.filter(id=delivery_id).delete()
        return deleted_count

    def get_unassigned_deliveries(self):
        return Delivery.objects.filter(route__isnull=True)
    
    def get_all_deliveries(self):
        return Delivery.objects.all().order_by('-created_at')

    def get_deliveries_for_route(self, route):
        return Delivery.objects.filter(route=route)
    
    def remove_delivery(self, delivery):
        delivery.delete()

    def clear_queue(self):
        deleted_count, _ = Delivery.objects.filter(route__isnull=True).delete()
        return deleted_count
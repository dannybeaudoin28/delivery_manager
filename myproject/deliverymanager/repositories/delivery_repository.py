from deliverymanager.models import Delivery

class DeliveryRepository:
    
    def add_or_update_delivery(self, delivery):
        delivery.save()
        return delivery

    def remove_delivery(self, delivery_id):
        deleted_count, _ = Delivery.objects.filter(id=delivery_id).delete()
        return deleted_count

    def get_unassigned_deliveries(self):
        return Delivery.objects.filter(status=Delivery.STATUS_UNASSIGNED)
    
    def get_delivery_by_id(self, id):
        print("inside repo ID is: " + str(id))
        return Delivery.objects.get(id=id)
    
    def get_all_deliveries(self):
        return Delivery.objects.all().order_by('-created_at')

    def get_deliveries_for_route(self, route):
        return Delivery.objects.filter(route=route)
    
    def remove_delivery(self, delivery):
        delivery.delete()

    def clear_queue(self):
        deleted_count, _ = Delivery.objects.filter(
            status=Delivery.STATUS_UNASSIGNED,
        ).delete()
        return deleted_count
    
    def assign_deliveries_to_route(self, deliveries, route):
        for delivery in deliveries:
            delivery.route = route
            save()
            
    def mark_delivered(self, delivery):
        delivery.status = Delivery.STATUS_DELIVERED
        delivery.route = None
        delivery.route_order = None
        delivery.leg_distance_meters = None
        delivery.leg_duration_seconds = None
        delivery.save()
        return delivery
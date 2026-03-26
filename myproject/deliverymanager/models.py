from django.db import models

class Route(models.Model):
    total_time = models.FloatField()
    total_distance = models.FloatField()
    
class Driver(models.Model):
    name = models.CharField(max_length=30)
    route = models.OneToOneField(Route, on_delete=models.SET_NULL, null=True)
    
class Delivery(models.Model):
    STATUS_UNASSIGNED = "Unassigned"
    STATUS_ASSIGNED = "Assigned"
    STATUS_DELIVERED = "Delivered"

    STATUS_CHOICES = [
        (STATUS_UNASSIGNED, "Unassigned"),
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_DELIVERED, "Delivered"),
    ]
    
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_custom = models.BooleanField(default=False)
    
    route = models.ForeignKey(
        Route, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='deliveries'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_UNASSIGNED
    )

    route_order = models.IntegerField(null=True, blank=True)
    leg_distance_meters = models.FloatField(null=True, blank=True)
    leg_duration_seconds = models.IntegerField(null=True, blank=True)
    
    def get_created_at(self):
        return self.created_at
    
class CustomDelivery(Delivery):
    priority_level = models.IntegerField()
    scheduled_time = models.DateTimeField()

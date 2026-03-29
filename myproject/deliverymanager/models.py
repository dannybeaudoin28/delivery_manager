from django.db import models


class Route(models.Model):
    """
    Represents a generated delivery route with aggregated metrics.
    """
    total_time = models.FloatField()
    total_distance = models.FloatField()
    

class Driver(models.Model):
    """
    Represents a driver who may be assigned to a single route.
    """
    name = models.CharField(max_length=30)

    # One-to-one relationship ensures a driver has at most one active route
    route = models.OneToOneField(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        related_name="driver"
    )
    

class Delivery(models.Model):
    """
    Base delivery model representing a single delivery task.
    """

    # Delivery status constants
    STATUS_UNASSIGNED = "Unassigned"
    STATUS_ASSIGNED = "Assigned"
    STATUS_DELIVERED = "Delivered"

    STATUS_CHOICES = [
        (STATUS_UNASSIGNED, "Unassigned"),
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_DELIVERED, "Delivered"),
    ]
    
    address = models.CharField(max_length=200)

    # Coordinates resolved via geocoding service
    latitude = models.FloatField()
    longitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    # Indicates whether this is a custom (extended) delivery type
    is_custom = models.BooleanField(default=False)
    
    # Optional relationship to a route (null when unassigned)
    route = models.ForeignKey(
        Route, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='deliveries'
    )
    
    # Current lifecycle state of the delivery
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_UNASSIGNED
    )

    # Position of this delivery within a route
    route_order = models.IntegerField(null=True, blank=True)

    # Per-leg metrics calculated during route generation
    leg_distance_meters = models.FloatField(null=True, blank=True)
    leg_duration_seconds = models.IntegerField(null=True, blank=True)
    
    def get_created_at(self):
        """
        Accessor for creation timestamp (used for sorting/display).
        """
        return self.created_at
    

class CustomDelivery(Delivery):
    """
    Extended delivery type with scheduling and priority.
    """

    # Lower values indicate higher priority
    priority_level = models.IntegerField()

    # Scheduled delivery time for custom deliveries
    scheduled_time = models.DateTimeField()
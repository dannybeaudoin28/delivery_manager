from django.db import models

class Delivery(models.Model):
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def get_created_at(self):
        return self.created_at
    
class CustomDelivery(Delivery):
    priority_level = models.IntegerField()
    scheduled_time = models.DateTimeField()
    
class Route(models.Model):
    deliveries = models.ManyToManyField(Delivery)
    total_time = models.FloatField()
    total_distance = models.FloatField()
    
class Driver(models.Model):
    name = models.CharField(max_length=30)
    route = models.OneToOneField(Route, on_delete=models.SET_NULL, null=True)
    

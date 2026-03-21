from django.db import models

class Delivery(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200)
    latitude = models.FloatField(default=000000.00)
    longitude = models.FloatField(default=000000.00)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True) 
    
    def get_created_at(self):
        return self.created_at
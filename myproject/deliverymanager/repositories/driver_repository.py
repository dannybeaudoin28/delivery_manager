from deliverymanager.models import Driver

class DriverRepository:
    
    def assign_route(self, driver):
        driver.save()
    
    def get_driver_by_id(self, driver_id):
            """
            Retrieve a driver by its primary key.

            Args:
                driver_id (int): Driver ID.

            Returns:
                Driver: Matching driver instance.
            """
            return Driver.objects.get(id=driver_id)
        
    def get_available_driver_ordered_by_name(self):
        return Driver.objects.filter(route__isnull=True).order_by("name")
    
    def get_drivers_ordered_by_route(self, route):
        return Driver.objects.filter(route=route).first()
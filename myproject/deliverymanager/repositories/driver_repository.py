from deliverymanager.models import Driver

class DriverRepository:
    
    def get_driver_by_id(self, driver_id):
            """
            Retrieve a driver by its primary key.

            Args:
                driver_id (int): Driver ID.

            Returns:
                Driver: Matching driver instance.
            """
            return Driver.objects.get(id=driver_id)
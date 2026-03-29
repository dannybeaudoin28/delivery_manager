from deliverymanager.models import Driver


class DriverRepository:
    """
    Repository responsible for all data access related to Driver entities.

    This keeps ORM queries out of higher-level layers (views, commands)
    and centralizes driver-related persistence and retrieval logic.
    """

    def save_driver(self, driver):
        """
        Persist changes to a driver, typically after assigning or updating a route.

        Args:
            driver (Driver): The driver instance to save.

        Returns:
            None
        """
        driver.save()
    
    def get_driver_by_id(self, driver_id):
        """
        Retrieve a driver by its primary key.

        Args:
            driver_id (int): Unique identifier for the driver.

        Returns:
            Driver: Matching driver instance.

        Raises:
            Driver.DoesNotExist: If no driver is found with the given ID.
        """
        return Driver.objects.filter(id=driver_id).first()
        
    def get_available_driver_ordered_by_name(self):
        """
        Retrieve all drivers that are not currently assigned to a route,
        ordered alphabetically by name.

        Returns:
            QuerySet: Available drivers ordered by name.
        """
        return Driver.objects.filter(route__isnull=True).order_by("name")
    
    def get_driver_by_route(self, route):
        """
        Retrieve the driver assigned to a specific route.

        Note:
            Despite the method name, this returns a single driver (or None),
            not a collection.

        Args:
            route (Route): The route to find the assigned driver for.

        Returns:
            Driver | None: The driver assigned to the route, if one exists.
        """
        return Driver.objects.filter(route=route).first()
    
    def exclude_null_routes(self):
        return Driver.objects.exclude(route__isnull=True)
from deliverymanager.commands.delivery_command import DeliveryCommand


# Command responsible for marking a delivery as completed
class MarkDeliveryDeliveredCommand(DeliveryCommand):

    # Constructor initializes required dependency:
    # - delivery_repository: handles retrieval and persistence of delivery data
    def __init__(self, driver_repository, delivery_repository, route_repository):
        self.driver_repository = driver_repository
        self.delivery_repository = delivery_repository
        self.route_repository = route_repository

    # Executes the process of marking a delivery as delivered
    def execute(self, id):
        # Retrieve the delivery object by ID
        delivery = self.delivery_repository.get_delivery_by_id(id)

        # Get the associated route (if any)
        route = delivery.route

        # Mark the delivery as delivered using the repository
        self.delivery_repository.mark_delivered(delivery)

        # If the delivery was part of a route, check if all deliveries are completed
        if route is not None:

            # Count remaining deliveries that are still assigned (not delivered)
            remaining = self.route_repository.count_remaining_deliveries(route)

            # If no deliveries remain, unassign the driver from the route
            if remaining == 0:

                # Find the driver assigned to this route
                driver = self.driver_repository.get_driver_by_route(route)

                # If a driver is found, remove the route assignment
                if driver:
                    driver.route = None
                    self.driver_repository.save_driver(driver)

        # Return the updated delivery object
        return delivery